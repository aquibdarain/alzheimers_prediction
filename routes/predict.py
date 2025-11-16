# routes/predict.py
import os, uuid
from flask import Blueprint, request, jsonify, current_app, send_file, url_for
from services.storage_service import save_upload, allowed_file
from services.model_service import predict as model_predict
from services.explain_service import make_gradcam
from services.report_service import generate_report

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

@predict_bp.route("/", methods=["POST"])
def predict_route():
    current_app.logger.info("Received prediction request")
    if "image" not in request.files:
        return jsonify({"error":"no image"}), 400

    f = request.files["image"]
    if f.filename == "" or not allowed_file(f.filename):
        return jsonify({"error":"invalid file"}), 400

    uniq = uuid.uuid4().hex
    img_path = save_upload(f, uniq)

    # preprocess and predict
    from utils.preprocess import preprocess
    try:
        img_tensor = preprocess(img_path)
        res = model_predict(img_tensor)
        current_app.logger.info("Model prediction: %s", res)
    except Exception as e:
        current_app.logger.exception("Prediction failed")
        return jsonify({"error":"prediction failed", "detail": str(e)}), 500

    # grad-cam
    heat_path = None
    try:
        heat_name = f"{uniq}_heat.jpg"
        heat_path = os.path.join(current_app.config.get("UPLOAD_DIR","uploads"), heat_name)
        make_gradcam(img_path, res.get("index"), heat_path)
    except Exception:
        current_app.logger.exception("Grad-CAM failed")
        heat_path = None

    # pdf
    pdf_path = None
    try:
        pdf_path = generate_report(uniq, img_path, heat_path, res.get("label"), res.get("probabilities"))
    except Exception:
        current_app.logger.exception("Report generation failed")
        pdf_path = None

    base = request.host_url.rstrip("/")
    heat_url = base + url_for("predict.get_heat", filename=os.path.basename(heat_path)) if heat_path and os.path.exists(heat_path) else None
    report_url = base + url_for("predict.get_report", filename=os.path.basename(pdf_path)) if pdf_path and os.path.exists(pdf_path) else None

    return jsonify({
        "label": res.get("label"),
        "probabilities": res.get("probabilities"),
        "heatmap_url": heat_url,
        "report_url": report_url
    }), 200

@predict_bp.route("/heat/<filename>", methods=["GET"])
def get_heat(filename):
    path = os.path.join(current_app.config.get("UPLOAD_DIR","uploads"), filename)
    if not os.path.exists(path):
        return jsonify({"error":"not found"}), 404
    return send_file(path, mimetype="image/jpeg")

@predict_bp.route("/report/<filename>", methods=["GET"])
def get_report(filename):
    path = os.path.join(current_app.config.get("UPLOAD_DIR","uploads"), filename)
    if not os.path.exists(path):
        return jsonify({"error":"not found"}), 404
    return send_file(path, mimetype="application/pdf")

@predict_bp.route("/", methods=["GET"])
def predict_info():
    current_app.logger.info("Predict info endpoint called")
    return jsonify({
        "status": "ok",
        "message": "Prediction service is up — use POST /predict/ with form-data 'image' to run inference."
    }), 200
