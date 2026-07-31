import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Handle database path resolution
    database_url = os.getenv("DATABASE_URL", "sqlite:///database/database.db")
    # If the URL is in sqlite:/// format, extract the relative path
    if database_url.startswith("sqlite:///"):
        db_rel_path = database_url[9:]
    else:
        db_rel_path = "database/database.db"
        
    # Get absolute path relative to this config file (backend/ directory)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    if not os.path.isabs(db_rel_path):
        DATABASE_PATH = os.path.abspath(os.path.join(BASE_DIR, db_rel_path))
    else:
        DATABASE_PATH = db_rel_path

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
