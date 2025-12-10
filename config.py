import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH")
LIBPAFE_PATH = os.getenv("LIBPAFE_PATH")
GOOGLE_JSON_PATH = os.getenv("GOOGLE_JSON_PATH")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
