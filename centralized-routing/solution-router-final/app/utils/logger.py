"""Logger for the router application."""
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "../../app/data")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, "router.log")),
    ],
)
logger = logging.getLogger("router")
