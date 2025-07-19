"""
Application configuration and settings.
"""

import os

# Application Information
APP_NAME = "Cowriter"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Window Settings
WINDOW_TITLE = APP_NAME
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_MIN_WIDTH = 600
WINDOW_MIN_HEIGHT = 400

# Theme Settings
THEME = "dark"  # "light" or "dark"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
CONFIG_DIR = os.path.join(os.path.dirname(__file__))

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Application Settings
AUTO_SAVE = True
AUTO_SAVE_INTERVAL = 300  # seconds
