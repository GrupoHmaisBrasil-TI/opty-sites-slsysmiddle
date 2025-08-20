from pathlib import Path
from dotenv import load_dotenv 
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = "appointments_sadalla.csv"
QUERY_FILE = "query.sql"
APPOINTMENTS_FILE = BASE_DIR / "file" / DATA_FILE
SQL_FILE = BASE_DIR / "sql" / QUERY_FILE

DB_HOST = os.getenv("DB_HOST", {})
DB_NAME = os.getenv("DB_NAME", {})
DB_USER = os.getenv("DB_USER", {})
DB_PASSWORD = os.getenv("DB_PASSWORD", {})
SFTP_HOST = os.getenv("SFTP_HOST", {})
SFTP_USER = os.getenv("SFTP_USER", {})
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", {})