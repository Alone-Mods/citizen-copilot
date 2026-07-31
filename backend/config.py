import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration class that loads values from environment variables
    or provides secure default values.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Absolute base directory of the backend folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database configuration path resolution
    database_url = os.getenv("DATABASE_URL", "sqlite:///database/database.db")
    if database_url.startswith("sqlite:///"):
        # Slice out the prefix (10 characters: 'sqlite:///')
        db_rel_path = database_url[10:]
    else:
        db_rel_path = "database/database.db"
        
    # Construct an absolute database path relative to backend directory
    if not os.path.isabs(db_rel_path):
        DATABASE_PATH = os.path.abspath(os.path.join(BASE_DIR, db_rel_path))
    else:
        DATABASE_PATH = db_rel_path

    # Gemini AI configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Document upload configurations
    UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "uploads"))
    
    # Max file upload size: 5MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
