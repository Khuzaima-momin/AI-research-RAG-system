import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = "research-assistant-secret-key"

    UPLOAD_FOLDER = "uploads"

    VECTOR_DB = "vector_db"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024