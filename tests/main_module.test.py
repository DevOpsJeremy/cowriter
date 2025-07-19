"""
Unit tests for the __main__ module entry point.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import src.__main__

class TestMainModule(unittest.TestCase):
    """Test cases for the __main__ module."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    @patch('src.__main__.Application')
    def test_main_function_exists(self, mock_application):
        """Test that the main function exists and is callable."""
        self.assertTrue(hasattr(src.__main__, 'main'))
        self.assertTrue(callable(getattr(src.__main__, 'main')))
    
    @patch('src.__main__.Application')
    def test_main_function_creates_application(self, mock_application):
        """Test that the main function creates an Application instance."""
        mock_app_instance = Mock()
        mock_application.return_value = mock_app_instance
        
        src.__main__.main()
        
        # Verify that Application was instantiated
        mock_application.assert_called_once()
        
        # Verify that run was called on the application instance
        mock_app_instance.run.assert_called_once()
    
    @patch('src.__main__.Application')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_function_handles_keyboard_interrupt(self, mock_print, mock_exit, mock_application):
        """Test that the main function handles KeyboardInterrupt gracefully."""
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = KeyboardInterrupt()
        mock_application.return_value = mock_app_instance
        
        src.__main__.main()
        
        # Verify that a message was printed
        mock_print.assert_called_with("\nApplication interrupted by user")
        
        # Verify that sys.exit was called with code 0
        mock_exit.assert_called_once_with(0)
    
    @patch('src.__main__.Application')
    @patch('sys.exit')
    @patch('builtins.print')
    def test_main_function_handles_general_exception(self, mock_print, mock_exit, mock_application):
        """Test that the main function handles general exceptions."""
        test_error = Exception("Test error message")
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = test_error
        mock_application.return_value = mock_app_instance
        
        src.__main__.main()
        
        # Verify that an error message was printed
        mock_print.assert_called_with(f"An error occurred: {test_error}")
    
    @patch('src.__main__.Application')
    def test_main_function_application_creation_failure(self, mock_application):
        """Test that the main function handles Application creation failure."""
        mock_application.side_effect = Exception("Application creation failed")
        
        # This should not raise an exception, it should be caught and handled
        try:
            src.__main__.main()
        except Exception:
            self.fail("main() should handle Application creation exceptions gracefully")
    
    def test_module_docstring(self):
        """Test that the module has a proper docstring."""
        self.assertIsNotNone(src.__main__.__doc__)
        self.assertTrue(len(src.__main__.__doc__.strip()) > 0)
        self.assertIn("entry point", src.__main__.__doc__.lower())


if __name__ == '__main__':
    unittest.main()
