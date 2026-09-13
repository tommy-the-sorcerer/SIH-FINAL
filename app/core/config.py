"""
Central Configuration for FALCON-AI Platform
Defines root-relative paths, environment settings, and secrets.
"""
import os
from pathlib import Path

# Project root directory (3 levels up from app/core/config.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Database configuration
DATABASE_PATH = Path(os.environ.get("FALCON_DB_PATH", PROJECT_ROOT / "falcon_ai.db"))

# Static assets and Jinja2 templates
STATIC_DIR = PROJECT_ROOT / "static"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
UPLOADS_DIR = STATIC_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Machine Learning Model Checkpoints
MODEL_PATHS = [
    PROJECT_ROOT / "Models" / "PlantDiseaseDetection.pt",
    PROJECT_ROOT / "models" / "PlantDiseaseDetection.pt",
    Path("Models/PlantDiseaseDetection.pt"),
    Path("models/PlantDiseaseDetection.pt"),
]

# Security & Secrets
AUTH_SECRET_KEY = os.environ.get("FALCON_AUTH_SECRET", "falcon_ai_sih26131_production_secret_key_2026")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# File upload limits
MAX_UPLOAD_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
