# app.py - create_app and register blueprints
from flask import Flask
from utils.logging_config import init_logging
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

     # <-- Add this
    # Allow only your frontend origin in production (example below)
    # For development you can allow all origins, but restrict in production.
    FRONTEND_ORIGINS = ["http://localhost:3000"]  # change to your frontend URL
    CORS(app, resources={r"/*": {"origins": FRONTEND_ORIGINS}}, supports_credentials=True)
    # -->
    CORS(app)   # WARNING: allows all origins

    # initialize logging
    init_logging(app)

    # register blueprints
    from routes.health import health_bp
    from routes.predict import predict_bp  # safe to import now (file may be placeholder)
    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)

    app.logger.info("Application created and blueprints registered")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
