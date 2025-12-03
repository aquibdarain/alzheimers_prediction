# models/result.py
from services.db import db
from datetime import datetime

class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    uuid = db.Column(db.String(64), nullable=False, unique=True)

    # file paths (store relative path or S3 key)
    image_path = db.Column(db.String(512), nullable=False)
    heatmap_path = db.Column(db.String(512), nullable=True)
    report_path = db.Column(db.String(512), nullable=True)

    # prediction details
    label = db.Column(db.String(64), nullable=True)
    prob_normal = db.Column(db.Float, nullable=True)
    prob_mci = db.Column(db.Float, nullable=True)
    prob_alzheimer = db.Column(db.Float, nullable=True)

    suggestion_text = db.Column(db.Text, nullable=True)
    review_status = db.Column(db.String(32), default="pending")
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # relationship
    patient = db.relationship("Patient", backref=db.backref("results", lazy="dynamic"))
