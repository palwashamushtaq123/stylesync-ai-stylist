import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

# Supported local Pakistani brands
PAK_BRANDS = [
    "Khaadi",
    "Junaid Jamshed (J.)",
    "Gul Ahmed",
    "Sapphire",
    "Limelight",
    "Bonanza Satrangi",
    "Sana Safinaz",
    "Alkaram Studio",
    "Outfitters"
]