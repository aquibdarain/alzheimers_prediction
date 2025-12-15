# # config.py
# import os
# from dotenv import load_dotenv
# load_dotenv(override=True)  # or better:
# load_dotenv(override=True, interpolate=True)

# load_dotenv()   # Load .env file

# class Config:
#     # Database
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # App settings
#     UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
#     LOG_DIR = os.getenv("LOG_DIR", "logs")
#     MODEL_PATH = os.getenv("MODEL_PATH", "model/alzheimer_model.pth")

#     DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

# # Ensure folders exist
# os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
# os.makedirs(Config.LOG_DIR, exist_ok=True)
# os.makedirs(os.path.dirname(Config.MODEL_PATH) or ".", exist_ok=True)





# config.py
import os
from dotenv import load_dotenv

# Load .env with proper variable interpolation support (so you CAN use ${VAR} syntax if you want later)
load_dotenv(override=True)

class Config:
    """Central configuration class"""

    # ───────────────────────────────────────
    # DATABASE
    # ───────────────────────────────────────
    # Current (SQLite):   DATABASE_URL=sqlite:///alzheimers.db
    # Future (MySQL):     DATABASE_URL=mysql+pymysql://root:root@localhost:3306/alzheimers_db
    # Future (PostgreSQL):DATABASE_URL=postgresql://user:pass@host:5432/alzheimers_db
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///alzheimers.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True only if you want to debug SQL queries

    # ───────────────────────────────────────
    # APP SETTINGS
    # ───────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production-2025")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Folders & Paths
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    MODEL_PATH = os.getenv("MODEL_PATH", "model/alzheimer_model.pth")

    # ───────────────────────────────────────
    # OPTIONAL: Max upload size (5MB default)
    # ───────────────────────────────────────
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit for MRI images


# ───────────────────────────────────────────
# Create required directories at startup
# ───────────────────────────────────────────
def init_directories():
    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    model_dir = os.path.dirname(Config.MODEL_PATH)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)

# Run on import (safe in Flask context)
init_directories()