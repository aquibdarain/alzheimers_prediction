# create_tables.py
from app import create_app
from services.db import db
import sys

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ Tables created (db.create_all())")
    except Exception as e:
        print("❌ Failed to create tables:", e)
        sys.exit(1)
