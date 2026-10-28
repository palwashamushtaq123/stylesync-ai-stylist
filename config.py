config_code = '''import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file for local development
load_dotenv()

# Get API key from Streamlit Cloud Secrets first, then fallback to environment variables (.env)
GROQ_API_KEY = ""
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not GROQ_API_KEY:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Get Model from Secrets or env or default
GROQ_MODEL = ""
try:
    if "GROQ_MODEL" in st.secrets:
        GROQ_MODEL = st.secrets["GROQ_MODEL"]
except Exception:
    pass

if not GROQ_MODEL:
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
'''.replace("GROQ_MODEL = os.getenv", "    GROQ_MODEL = os.getenv")

with open("config.py", "w", encoding="utf-8") as f:
    f.write(config_code)

print("config.py updated successfully!")