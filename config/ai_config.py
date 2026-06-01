import os
from dotenv import load_dotenv
from groq import Client

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in .env")

GROQ_API_KEY_VISION = os.getenv("GROQ_API_KEY_VISION")

GROQ_CLIENT = Client(api_key=GROQ_API_KEY)
GROQ_CLIENT_VISION = Client(api_key=GROQ_API_KEY_VISION) if GROQ_API_KEY_VISION else GROQ_CLIENT