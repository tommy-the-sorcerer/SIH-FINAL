"""
Pytest configuration and environment initialization for FALCON-AI test suite.
Injects app, core, and services onto sys.path to guarantee backward compatibility.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
app_dir = PROJECT_ROOT / "app"
core_dir = app_dir / "core"
services_dir = app_dir / "services"

for p in [str(PROJECT_ROOT), str(app_dir), str(core_dir), str(services_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)
