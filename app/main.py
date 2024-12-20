import logging
import os
from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager

from app.database import Base, Calculation  # Import Base and Calculation model
from app.operations import addition, subtraction, multiplication, division
from app.groq_api import call_groq_function  
from pydantic import BaseModel
# ================== CONFIGURE LOGGING ==================
log_file_path = os.getenv("LOG_FILE_PATH", "app.log")  # Use environment variable or default
is_testing = os.getenv("TESTING", "false").lower() == "true"  # Check if testing mode is enabled

handlers = [logging.StreamHandler()]  # Always log to the console
if not is_testing:  # Add FileHandler only if not in testing mode
    handlers.append(logging.FileHandler(log_file_path))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=handlers,
)

logger = logging.getLogger(__name__)

# ================== DATABASE CONFIGURATION ==================
DATABASE_URL = "postgresql://postgres:password@db:5432/calculator_db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# ================== LIFESPAN EVENT ==================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables at startup and clean up resources on shutdown."""
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)  # Create tables
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    try:
        yield
    finally:
        try:
            logger.info("Application shutdown...")
        except Exception as e:
            logger.error(f"Error during application shutdown: {e}")



# FastAPI app instance with lifespan
app = FastAPI(lifespan=lifespan)

# Dependency to get the database session
def get_db():
    logger.info("Creating database session...")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Database session closed.")

# ================== STATIC FILES ==================
app.mount("/static", StaticFiles(directory="static"), name="static")

# ================== ROUTES ==================

# Serve the frontend calculator HTML
@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the frontend calculator HTML."""
    try:
        with open("static/index.html") as file:
            logger.info("Serving index.html.")
            return HTMLResponse(content=file.read(), status_code=200)
    except FileNotFoundError as e:
        logger.error(f"Static file not found: {e}")
        raise HTTPException(status_code=404, detail="Static file not found.")

# Perform calculations and save them to the database
@app.post("/")
async def calculate(
    operation: str = Query(...), num1: float = Query(...), num2: float = Query(...), db: Session = Depends(get_db)
):
    """Perform calculations using imported functions and save to the database."""
    try:
        logger.info(f"Received calculation request: operation={operation}, num1={num1}, num2={num2}")
        operations_map = {
            "add": addition,
            "subtract": subtraction,
            "multiply": multiplication,
            "divide": division,
        }

        if operation not in operations_map:
            logger.warning(f"Invalid operation requested: {operation}")
            return JSONResponse({"error": "Invalid operation"}, status_code=400)

        result = operations_map[operation](num1, num2)
        logger.info(f"Calculation result: {result}")

        # Save the calculation to the database
        db_calc = Calculation(operation=operation, num1=num1, num2=num2, result=result)
        db.add(db_calc)
        try:
            db.commit()
        except Exception as e:
            logger.error(f"Database commit error: {e}")
            return JSONResponse({"error": "Internal server error"}, status_code=500)
        db.refresh(db_calc)

        logger.info(f"Calculation saved to database with ID: {db_calc.id}")
        return {"result": result, "id": db_calc.id}
    except ValueError as e:
        logger.error(f"ValueError during calculation: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)  # Ensure this exists


# Fetch all calculations from the database
@app.get("/calculations")
async def get_calculations(db: Session = Depends(get_db)):
    """Retrieve all stored calculations."""
    logger.info("Fetching all calculations from the database.")
    calculations = db.query(Calculation).all()
    logger.info(f"Retrieved {len(calculations)} calculations.")
    return calculations

class CalculationRequest(BaseModel):
    operation: str
    a: float
    b: float

# Update the `/groq-calculate` route to use the Pydantic model
@app.post("/groq-calculate")
async def groq_calculate(request: CalculationRequest):
    try:
        logger.info(f"Calling GroqAPI for calculation: operation={request.operation}, a={request.a}, b={request.b}")
        response = call_groq_function(request.operation, {"a": request.a, "b": request.b})
        logger.info(f"GroqAPI response: {response}")
        return {"operation": request.operation, "result": response.get("result")}
    except Exception as e:
        logger.error(f"Error during GroqAPI calculation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class AskRequest(BaseModel):
    question: str

@app.post("/groq-ask")
async def groq_ask(request: AskRequest):
    """
    Ask a natural language question and receive a response from the LLM.
    """
    try:
        logger.info(f"Calling GroqAPI for question: {request.question}")
        response = call_groq_function("ask_question", {"question": request.question})
        logger.info(f"GroqAPI response: {response}")
        return {"question": request.question, "response": response.get("response")}
    except Exception as e:
        logger.error(f"Error during GroqAPI interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


