import os
from dotenv import load_dotenv
from groq import Client

# Load environment variables from .env
load_dotenv()

# Get the API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")

GROQ_CLIENT = Client(api_key=GROQ_API_KEY)