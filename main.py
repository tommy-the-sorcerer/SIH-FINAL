"""
FALCON-AI Root Application Entry Point
Supports running with:
- uvicorn main:app --reload
- python main.py
Provides backward-compatible exports for all existing tests and scripts.
"""
import sys
import os
from pathlib import Path

# Ensure all modular package directories are in sys.path for seamless imports
PROJECT_ROOT = Path(__file__).resolve().parent
app_dir = PROJECT_ROOT / "app"
core_dir = app_dir / "core"
services_dir = app_dir / "services"

for p in [str(PROJECT_ROOT), str(app_dir), str(core_dir), str(services_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import (
    app,
    create_access_token,
    verify_access_token,
    validate_and_sanitize_upload,
    is_valid_image_magic,
    AUTH_SECRET_KEY,
    MAX_UPLOAD_SIZE_BYTES,
    ALLOWED_EXTENSIONS,
)

__all__ = [
    "app",
    "create_access_token",
    "verify_access_token",
    "validate_and_sanitize_upload",
    "is_valid_image_magic",
    "AUTH_SECRET_KEY",
    "MAX_UPLOAD_SIZE_BYTES",
    "ALLOWED_EXTENSIONS",
]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)