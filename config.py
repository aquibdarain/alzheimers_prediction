# config.py
import os
from dotenv import load_dotenv

load_dotenv()   # Load .env file

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App settings
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    MODEL_PATH = os.getenv("MODEL_PATH", "model/alzheimer_model.pth")

    DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# Ensure folders exist
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(Config.MODEL_PATH) or ".", exist_ok=True)
