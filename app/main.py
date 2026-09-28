from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import create_tables
from .routes import router

BASE_DIR=Path(__file__).resolve().parent.parent
app=FastAPI(title=settings.APP_NAME, description="AI-powered fitness plan generator using Google Gemini.", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR/"static")), name="static")
@app.on_event("startup")
def startup(): create_tables()
@app.get("/health")
def health(): return {"status":"healthy","application":"FitBuddy"}
app.include_router(router)
