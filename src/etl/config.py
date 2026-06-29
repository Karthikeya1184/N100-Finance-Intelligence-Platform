from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = PROJECT_ROOT / "data" / "raw"

SUPPORTING_DATA = PROJECT_ROOT / "data" / "supporting"

OUTPUT_DIR = PROJECT_ROOT / "output"

DATABASE_PATH = PROJECT_ROOT / "db" / "nifty100.db"

LOGS_DIR = PROJECT_ROOT / "logs"