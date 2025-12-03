# app.py
from flask import Flask
from flask_cors import CORS
from utils.logging_config import init_logging
from services.db import init_db
from config import Config

# <-- new import
from services.db import init_db
# ensure models are imported when app starts so migrations detect them
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS (dev)
    FRONTEND_ORIGINS = ["http://localhost:3000"]
    CORS(app, resources={r"/*": {"origins": FRONTEND_ORIGINS}}, supports_credentials=True)
    CORS(app)   # WARNING: allows all origins

    # initialize logging
    init_logging(app)

    # initialize DB & migrations
    init_db(app)

    # register blueprints
    from routes.health import health_bp
    from routes.predict import predict_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)

    app.logger.info("Application created and blueprints registered")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)