# config.py
import os

class Config:
    # Basic folders (can be overridden by environment variables)
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
    MODEL_PATH = os.getenv("MODEL_PATH", "model/alzheimer_model.pth")
    LOG_DIR = os.getenv("LOG_DIR", "logs")

    # App behaviour
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB
    DEBUG = os.getenv("DEBUG", "False").lower() in ("1", "true", "yes")

    # Database (SQLAlchemy) — set DATABASE_URL in your env for production
    # Example: mysql+pymysql://dbuser:dbpass@localhost/alzheimers_db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/alzheimers_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Ensure folders exist when module is imported
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)
os.makedirs(os.path.dirname(Config.MODEL_PATH) or ".", exist_ok=True)
