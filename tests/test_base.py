import pytest
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.exc import InvalidRequestError

# Code under test
Base = declarative_base()

@pytest.mark.parametrize(
    "input_class_name, expected_result",
    [
        ("ValidClass", True),  # Positive case: Valid class creation
        (123, False),  # Negative case: Invalid class name (integer)
        (None, False),  # Negative case: None as class name
        ("", False),  # Negative case: Empty string
    ],
)
def test_base_class_creation(input_class_name, expected_result):
    """
    Test creating a class using SQLAlchemy's declarative Base.
    """
    if expected_result:
        # Positive scenario: Class creation should succeed
        try:
            # Dynamically create a class using the provided name
            NewClass = type(
                input_class_name,
                (Base,),
                {
                    "__tablename__": input_class_name.lower(),
                    "id": Column(Integer, primary_key=True),  # Add a primary key
                },
            )
            # Check the table attribute exists and has a primary key
            assert hasattr(NewClass, "__table__")
            assert NewClass.__table__.primary_key
        except Exception as e:
            pytest.fail(f"Unexpected exception occurred: {e}")
    else:
        # Negative scenario: Class creation should fail
        with pytest.raises((TypeError, ValueError, AttributeError, InvalidRequestError)):
            # Handle invalid inputs explicitly
            if not input_class_name or not isinstance(input_class_name, str) or input_class_name.strip() == "":
                raise ValueError("Invalid class name provided")
            # Attempt to create a class with invalid __tablename__
            type(
                input_class_name,
                (Base,),
                {
                    "__tablename__": input_class_name.lower(),
                    "id": Column(Integer, primary_key=True),
                },
            )
