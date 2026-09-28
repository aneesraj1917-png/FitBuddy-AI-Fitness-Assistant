import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    APP_NAME = "FitBuddy - AI Fitness Plan Generator"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-flash")
    GEMINI_NUTRITION_MODEL = os.getenv("GEMINI_NUTRITION_MODEL", "gemini-2.5-flash")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "fitbuddy-admin")
    AI_DEMO_MODE = os.getenv("AI_DEMO_MODE", "false").lower() == "true"

settings = Settings()
