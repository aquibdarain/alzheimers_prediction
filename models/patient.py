# models/patient.py
from services.db import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=True)
    doctor_name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "city": self.city,
            "doctor_name": self.doctor_name,
            "created_at": self.created_at
        }
