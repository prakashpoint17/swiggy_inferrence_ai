import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return its text response."""
    
    response = client.models.generate_content(
        model = MODEL,
        contents = prompt
    )
    
    return response.text