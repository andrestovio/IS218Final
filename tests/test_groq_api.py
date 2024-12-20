import pytest
import requests
from unittest.mock import patch, MagicMock
from app.groq_api import call_groq_function

@patch("app.groq_api.requests.post")
@patch("app.groq_api.API_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")
@patch("app.groq_api.API_KEY", "TEST_API_KEY")
def test_call_groq_function_success(mock_post):
    """
    Test that the function handles a successful API response correctly.
    """
    # Mock a successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_post.return_value = mock_response

    # Call the function
    result = call_groq_function("test_function", {"key": "value"})

    # Assertions
    assert result == {"result": "success"}
    mock_post.assert_called_once_with(
        "https://api.groq.com/openai/v1/chat/completions",  # Mocked API_ENDPOINT
        json={"function": "test_function", "inputs": {"key": "value"}},
        headers={
            "Authorization": "Bearer TEST_API_KEY",  # Mocked API_KEY
            "Content-Type": "application/json",
        },
    )

@patch("app.groq_api.requests.post")
@patch("app.groq_api.API_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")
@patch("app.groq_api.API_KEY", "TEST_API_KEY")
def test_call_groq_function_error(mock_post):
    """
    Test that the function raises an exception for non-200 status codes.
    """
    # Mock a failed API response
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
    mock_post.return_value = mock_response

    # Call the function and expect an exception
    with pytest.raises(requests.exceptions.HTTPError):
        call_groq_function("test_function", {"key": "value"})

    # Assertions
    mock_post.assert_called_once_with(
        "https://api.groq.com/openai/v1/chat/completions",
        json={"function": "test_function", "inputs": {"key": "value"}},
        headers={
            "Authorization": "Bearer TEST_API_KEY",
            "Content-Type": "application/json",
        },
    )

@patch("app.groq_api.requests.post")
@patch("app.groq_api.API_ENDPOINT", "https://api.groq.com/openai/v1/chat/completions")
@patch("app.groq_api.API_KEY", "TEST_API_KEY")
def test_call_groq_function_request_exception(mock_post):
    """
    Test that the function raises an exception when the request fails.
    """
    # Mock a network error
    mock_post.side_effect = requests.exceptions.RequestException("Network error")

    # Call the function and expect an exception
    with pytest.raises(requests.exceptions.RequestException):
        call_groq_function("test_function", {"key": "value"})

    # Assertions
    mock_post.assert_called_once_with(
        "https://api.groq.com/openai/v1/chat/completions",
        json={"function": "test_function", "inputs": {"key": "value"}},
        headers={
            "Authorization": "Bearer TEST_API_KEY",
            "Content-Type": "application/json",
        },
    )
