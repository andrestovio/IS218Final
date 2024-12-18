from fastapi import FastAPI, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager

from app.database import Base, Calculation  # Import Base and Calculation model
from app.operations import addition, subtraction, multiplication, division

# ================== DATABASE CONFIGURATION ==================
DATABASE_URL = "postgresql://postgres:password@db:5432/calculator_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ================== LIFESPAN EVENT ==================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables at startup and clean up resources on shutdown."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)  # Create tables
    yield
    print("Application shutdown...")

# FastAPI app instance with lifespan
app = FastAPI(lifespan=lifespan)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================== STATIC FILES ==================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================== ROUTES ==================

# Serve the frontend calculator HTML
@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the frontend calculator HTML."""
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read(), status_code=200)

# Perform calculations and save them to the database
@app.post("/")
async def calculate(
    operation: str = Query(...), num1: float = Query(...), num2: float = Query(...), db: Session = Depends(get_db)
):
    """Perform calculations using imported functions and save to the database."""
    try:
        # Determine the result based on the operation
        operations_map = {
            "add": addition,
            "subtract": subtraction,
            "multiply": multiplication,
            "divide": division,
        }

        if operation not in operations_map:
            return JSONResponse({"error": "Invalid operation"}, status_code=400)

        result = operations_map[operation](num1, num2)

        # Save the calculation to the database
        db_calc = Calculation(operation=operation, num1=num1, num2=num2, result=result)
        db.add(db_calc)
        db.commit()
        db.refresh(db_calc)

        # Return the calculation result and ID
        return {"result": result, "id": db_calc.id}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# Fetch all calculations from the database
@app.get("/calculations")
async def get_calculations(db: Session = Depends(get_db)):
    """Retrieve all stored calculations."""
    calculations = db.query(Calculation).all()
    return calculations
