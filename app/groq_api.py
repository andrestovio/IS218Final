import requests
from app.config import API_KEY, API_ENDPOINT

def call_groq_function(function_name, inputs):
    """
    Calls a GroqAPI function.
    
    Args:
        function_name (str): The name of the function to call.
        inputs (dict): The input parameters for the function.

    Returns:
        dict: The response from the API.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "function": function_name,
        "inputs": inputs,
    }

    response = requests.post(API_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
