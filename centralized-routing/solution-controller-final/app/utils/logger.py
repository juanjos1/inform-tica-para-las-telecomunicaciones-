"""Centralised logger for the controller application (FR-09)."""
import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "../../app/data")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "logs.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "controller.log")),
    ],
)

logger = logging.getLogger("controller")
