import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Fixture for overriding log file path
@pytest.fixture(scope="module", autouse=True)
def setup_logging(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("logs")
    log_file = temp_dir / "test_app.log"
    os.environ["LOG_FILE_PATH"] = str(log_file)
    yield log_file
    if log_file.exists():
        log_file.unlink()

# Fixture for mocking database session
@pytest.fixture
def mock_db_session():
    with patch("app.main.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        yield db

# Test static file not found (Lines 40-48)
def test_static_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        response = client.get("/")
        assert response.status_code == 404
        assert response.json() == {"detail": "Static file not found."}

# Test invalid operation (Lines 55-61)
def test_invalid_operation(mock_db_session):
    response = client.post("/", params={"operation": "invalid", "num1": 1, "num2": 2})
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid operation"}

# Test ValueError during calculation (Lines 76-78)
def test_value_error_during_calculation(mock_db_session):
    with patch("app.main.addition", side_effect=ValueError("Invalid input")):
        response = client.post("/", params={"operation": "add", "num1": 1, "num2": 2})
        assert response.status_code == 400
        assert response.json() == {"error": "Invalid input"}



# Test database commit failure (Lines 86-112)
def test_database_commit_failure(mock_db_session):
    # Mock the commit method to raise an exception
    mock_db_session.commit.side_effect = Exception("Database error")
    
    # Make the request to the calculate endpoint
    response = client.post("/", params={"operation": "add", "num1": 1, "num2": 2})
    
    # Ensure the response returns a 500 status code for the error
    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}


# Test GroqAPI calculation exception (Lines 118-121)
def test_groq_calculation_exception():
    with patch("app.main.call_groq_function", side_effect=Exception("GroqAPI error")):
        # Correct JSON payload for the request
        response = client.post("/groq-calculate", json={"operation": "add", "a": 1.0, "b": 2.0})
        assert response.status_code == 500
        assert response.json() == {"detail": "GroqAPI error"}




# Test GroqAPI natural language query exception (Lines 126-133)
def test_groq_natural_language_query_exception():
    with patch("app.main.call_groq_function", side_effect=Exception("GroqAPI error")):
        response = client.post("/groq-ask", json={"question": "What is AI?"})
        assert response.status_code == 500
        assert response.json() == {"detail": "GroqAPI error"}



# Test application shutdown (Lines 138-145)
def test_application_shutdown():
    with patch("app.main.logger") as mock_logger:
        with patch("app.main.Base.metadata.create_all") as mock_create_all:
            mock_create_all.side_effect = None  # Allow startup to succeed
            
            with patch("app.main.engine.connect", side_effect=Exception("Mocked shutdown error")):
                with client:
                    pass  # Simulate application lifecycle
        # Verify that the logger logs the shutdown message
        mock_logger.info.assert_any_call("Application shutdown...")



