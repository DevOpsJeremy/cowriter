"""
Unit tests for the configuration settings module.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings

class TestSettings(unittest.TestCase):
    """Test cases for the settings module."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    def test_app_info_constants(self):
        """Test that application information constants are defined correctly."""
        self.assertIsInstance(settings.APP_NAME, str)
        self.assertIsInstance(settings.APP_VERSION, str)
        self.assertIsInstance(settings.APP_AUTHOR, str)
        
        # Check that values are not empty
        self.assertTrue(len(settings.APP_NAME) > 0)
        self.assertTrue(len(settings.APP_VERSION) > 0)
        self.assertTrue(len(settings.APP_AUTHOR) > 0)
    
    def test_window_settings_types(self):
        """Test that window settings have correct types."""
        self.assertIsInstance(settings.WINDOW_TITLE, str)
        self.assertIsInstance(settings.WINDOW_WIDTH, int)
        self.assertIsInstance(settings.WINDOW_HEIGHT, int)
        self.assertIsInstance(settings.WINDOW_MIN_WIDTH, int)
        self.assertIsInstance(settings.WINDOW_MIN_HEIGHT, int)
    
    def test_window_settings_values(self):
        """Test that window settings have reasonable values."""
        # Window dimensions should be positive
        self.assertGreater(settings.WINDOW_WIDTH, 0)
        self.assertGreater(settings.WINDOW_HEIGHT, 0)
        self.assertGreater(settings.WINDOW_MIN_WIDTH, 0)
        self.assertGreater(settings.WINDOW_MIN_HEIGHT, 0)
        
        # Minimum dimensions should be smaller than or equal to default dimensions
        self.assertLessEqual(settings.WINDOW_MIN_WIDTH, settings.WINDOW_WIDTH)
        self.assertLessEqual(settings.WINDOW_MIN_HEIGHT, settings.WINDOW_HEIGHT)
    
    def test_theme_settings(self):
        """Test that theme settings are valid."""
        self.assertIsInstance(settings.THEME, str)
        self.assertIn(settings.THEME, ["light", "dark"])
    
    def test_path_settings(self):
        """Test that path settings are defined and are strings."""
        self.assertIsInstance(settings.BASE_DIR, str)
        self.assertIsInstance(settings.ASSETS_DIR, str)
        self.assertIsInstance(settings.CONFIG_DIR, str)
        
        # Paths should not be empty
        self.assertTrue(len(settings.BASE_DIR) > 0)
        self.assertTrue(len(settings.ASSETS_DIR) > 0)
        self.assertTrue(len(settings.CONFIG_DIR) > 0)
    
    def test_logging_settings(self):
        """Test that logging settings are valid."""
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        self.assertIsInstance(settings.LOG_LEVEL, str)
        self.assertIn(settings.LOG_LEVEL, valid_log_levels)
        
        self.assertIsInstance(settings.LOG_FORMAT, str)
        self.assertTrue(len(settings.LOG_FORMAT) > 0)
        
        # Check that format string contains common format specifiers
        self.assertIn("%(asctime)s", settings.LOG_FORMAT)
        self.assertIn("%(name)s", settings.LOG_FORMAT)
        self.assertIn("%(levelname)s", settings.LOG_FORMAT)
        self.assertIn("%(message)s", settings.LOG_FORMAT)
    
    def test_application_settings(self):
        """Test that application settings are valid."""
        self.assertIsInstance(settings.AUTO_SAVE, bool)
        self.assertIsInstance(settings.AUTO_SAVE_INTERVAL, int)
        
        # Auto save interval should be positive
        self.assertGreater(settings.AUTO_SAVE_INTERVAL, 0)
    
    def test_constants_immutability(self):
        """Test that important constants are defined as expected."""
        # Test that we can read the constants without errors
        app_name = settings.APP_NAME
        window_width = settings.WINDOW_WIDTH
        theme = settings.THEME
        
        # These should all be accessible
        self.assertIsNotNone(app_name)
        self.assertIsNotNone(window_width)
        self.assertIsNotNone(theme)


if __name__ == '__main__':
    unittest.main()
