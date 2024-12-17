from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from app.operations import addition, subtraction, multiplication, division

app = FastAPI()

# Serve static files (CSS/JS) from 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the frontend calculator HTML."""
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.post("/")
async def calculate(operation: str = Query(...), num1: float = Query(...), num2: float = Query(...)):
    """Perform calculations using imported functions."""
    try:
        # Call the respective operation function
        if operation == "add":
            result = addition(num1, num2)
        elif operation == "subtract":
            result = subtraction(num1, num2)
        elif operation == "multiply":
            result = multiplication(num1, num2)
        elif operation == "divide":
            result = division(num1, num2)
        else:
            return JSONResponse({"error": "Invalid operation"}, status_code=400)

        # Return the result
        return {"result": result}
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)
