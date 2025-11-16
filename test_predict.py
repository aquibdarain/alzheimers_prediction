# test_predict.py — runs a quick local prediction inside the Flask app context
from app import create_app
from utils.preprocess import preprocess
from services.model_service import load_model, predict

app = create_app()
with app.app_context():
    print("App context active. Loading model...")
    load_model()
    t = preprocess("uploads/test.jpg")   # ensure this file exists
    res = predict(t)
    print("Prediction result:", res)
