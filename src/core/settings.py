import os
import logging
from pathlib import Path
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv,find_dotenv

logger = logging.getLogger("uvicorn.error")
load_dotenv()

BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR.parent / "public"
CREDENTIALS = {
    'ENDPOINT_HML': os.environ.get("ENDPOINT_HML"),
    'ENDPOINT_PRD': os.environ.get("ENDPOINT_PRD"),
    'APIKEY': os.environ.get("APIKEY")
}

templates = Jinja2Templates(directory=str(STATIC_DIR))