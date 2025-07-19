"""
Application configuration and settings.
"""

from pathlib import Path

# Application Information
APP_NAME = "Cowriter"
APP_VERSION = "1.0.0"
APP_AUTHOR = "DevOpsJeremy"

# Window Settings
WINDOW_TITLE = APP_NAME
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400

# Theme Settings
THEME = "dark"  # "light" or "dark"

# Paths - Using pathlib for better cross-platform compatibility
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = SRC_DIR / "assets"
CONFIG_DIR = SRC_DIR / "config"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Application Settings
AUTO_SAVE = True
AUTO_SAVE_INTERVAL = 300  # seconds
