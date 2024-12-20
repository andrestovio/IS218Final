from dotenv import load_dotenv
import os

load_dotenv()

API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("API_KEY")