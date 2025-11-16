# utils/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

def init_logging(app):
    log_dir = app.config.get("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "service.log")

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if not app.config.get("DEBUG") else logging.DEBUG)

    # Rotating file handler
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.INFO)
    file_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(file_fmt)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.config.get("DEBUG") else logging.INFO)
    console_handler.setFormatter(file_fmt)

    # Avoid duplicate handlers when reloading
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    else:
        # replace existing handlers with these (helps when restarting)
        logger.handlers = [file_handler, console_handler]

    # Also attach the configured handlers to Flask's app.logger
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    app.logger.info("Logging initialized (level=%s) - log file: %s", logging.getLevelName(logger.level), log_file)
