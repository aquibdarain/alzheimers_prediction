from app import create_app
from services.model_service import load_model, predict
from services.explain_service import make_gradcam
from services.report_service import generate_report
from utils.preprocess import preprocess
import os, uuid

app = create_app()
with app.app_context():
    load_model()
    src = "uploads/test.jpg"    # ensure this exists
    uniq = uuid.uuid4().hex
    heat_path = os.path.join(app.config["UPLOAD_DIR"], f"{uniq}_heat.jpg")
    make_gradcam(src, None, heat_path)
    print("Heatmap saved to:", heat_path)

    t = preprocess(src)
    res = predict(t)
    pdf = generate_report(uniq, src, heat_path, res["label"], res["probabilities"])
    print("PDF generated:", pdf)
