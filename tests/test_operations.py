import pytest
from app.operations import addition, subtraction, multiplication, division

# Tests for addition
@pytest.mark.parametrize("a, b, expected", [
    (1.5, 2.5, 4.0),      # Positive case
    (-1.5, -2.5, -4.0),   # Positive case
    (10.0, 5.0, 15.0),    # Positive case
    (0, 5.0, 5.0),        # Positive case
    (2.0, 3.0, 6.0)       # Negative case: Expected result is incorrect
])
def test_addition(a, b, expected):
    if (a + b) == expected:  # Positive outcome
        assert addition(a, b) == expected
    else:  # Negative outcome
        assert addition(a, b) != expected

# Tests for subtraction
@pytest.mark.parametrize("a, b, expected", [
    (5.0, 3.0, 2.0),       # Positive case
    (10.0, 5.0, 5.0),      # Positive case
    (-10.0, -5.0, -5.0),   # Positive case
    (0.0, 5.0, -5.0),      # Positive case
    (5.0, 3.0, 1.0)        # Negative case: Expected result is incorrect
])
def test_subtraction(a, b, expected):
    if (a - b) == expected:  # Positive outcome
        assert subtraction(a, b) == expected
    else:  # Negative outcome
        assert subtraction(a, b) != expected

# Tests for multiplication
@pytest.mark.parametrize("a, b, expected", [
    (2.0, 3.0, 6.0),       # Positive case
    (-2.0, 3.0, -6.0),     # Positive case
    (0.0, 5.0, 0.0),       # Positive case
    (-3.0, -2.0, 6.0),     # Positive case
    (2.0, 3.0, 7.0)        # Negative case: Expected result is incorrect
])
def test_multiplication(a, b, expected):
    if (a * b) == expected:  # Positive outcome
        assert multiplication(a, b) == expected
    else:  # Negative outcome
        assert multiplication(a, b) != expected

# Tests for division
@pytest.mark.parametrize("a, b, expected", [
    (6.0, 3.0, 2.0),       # Positive case
    (5.0, 2.5, 2.0),       # Positive case
    (-10.0, 2.0, -5.0),    # Positive case
    (0.0, 3.0, 0.0),       # Positive case
    (6.0, 3.0, 3.0)        # Negative case: Expected result is incorrect
])
def test_division(a, b, expected):
    if b == 0:
        pytest.skip("Skipping division by zero in this test")
    if (a / b) == expected:  # Positive outcome
        assert division(a, b) == expected
    else:  # Negative outcome
        assert division(a, b) != expected

# Test for division by zero
@pytest.mark.parametrize("a, b", [
    (10.0, 0),
    (0.0, 0)
])
def test_division_by_zero(a, b):
    with pytest.raises(ValueError, match="division by zero is not allowed."):
        division(a, b)
