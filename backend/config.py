import os

class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
