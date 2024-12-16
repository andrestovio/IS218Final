def addition(a: float, b: float) -> float:
    """This function takes two float numbers as arguments and returns their sum."""
    result = a + b
    return result

def subtraction(a: float, b: float) -> float:
    """Returns the result of subtracting the second number from the first."""
    result = a - b
    return result

def multiplication(a: float, b: float) -> float:
    """This function takes two float numbers as arguments and returns their product."""
    result = a * b
    return result

def division(a: float, b: float) -> float:
    """Returns the result of dividing the first number by the second."""
    if b == 0:
        raise ValueError("division by zero is not allowed.")
    
    result = a / b
    return result
