"""
Unit tests for the main application class.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.app import Application

class TestApplication(unittest.TestCase):
    """Test cases for the Application class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock tkinter to avoid GUI creation during tests
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.winfo_width.return_value = 800
        self.mock_root.winfo_height.return_value = 600
        self.mock_root.winfo_screenwidth.return_value = 1920
        self.mock_root.winfo_screenheight.return_value = 1080
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_application_initialization(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the application initializes correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        
        # Verify that Tk was called to create the root window
        mock_tk.assert_called_once()
        
        # Verify that logging was set up
        mock_logging.basicConfig.assert_called_once()
        
        # Verify that the main window was created
        mock_main_window.assert_called_once_with(self.mock_root)
        
        # Verify that the app has the expected attributes
        self.assertIsNotNone(app.root)
        self.assertIsNotNone(app.main_window)
        self.assertIsNotNone(app.logger)
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_setup_logging(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that logging is set up correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        
        # Verify logging.basicConfig was called with correct parameters
        mock_logging.basicConfig.assert_called_once()
        call_args = mock_logging.basicConfig.call_args
        self.assertIn('level', call_args.kwargs)
        self.assertIn('format', call_args.kwargs)
        self.assertIn('handlers', call_args.kwargs)
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_setup_root_window(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the root window is configured correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        
        # Verify that window properties were set
        self.mock_root.title.assert_called()
        self.mock_root.geometry.assert_called()
        self.mock_root.minsize.assert_called()
        self.mock_root.protocol.assert_called_with("WM_DELETE_WINDOW", app.on_closing)
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_center_window(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the window centering calculation works correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        app.center_window()
        
        # Verify that update_idletasks was called
        self.mock_root.update_idletasks.assert_called()
        
        # Verify that geometry was called (window positioning)
        self.assertTrue(self.mock_root.geometry.call_count >= 2)  # Once in setup, once in center
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_setup_theme(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the theme is set up correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        
        # Verify that sv_ttk.set_theme was called
        mock_sv_ttk.set_theme.assert_called_once()
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_on_closing(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the application closes correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        app.on_closing()
        
        # Verify that quit and destroy were called
        self.mock_root.quit.assert_called_once()
        self.mock_root.destroy.assert_called_once()
    
    @patch('src.app.tk.Tk')
    @patch('src.app.MainWindow')
    @patch('src.app.sv_ttk')
    @patch('src.app.logging')
    def test_run(self, mock_logging, mock_sv_ttk, mock_main_window, mock_tk):
        """Test that the application runs correctly."""
        mock_tk.return_value = self.mock_root
        
        app = Application()
        app.run()
        
        # Verify that mainloop was called
        self.mock_root.mainloop.assert_called_once()


class TestApplicationMain(unittest.TestCase):
    """Test cases for the main function."""
    
    @patch('src.app.Application')
    def test_main_function_success(self, mock_application):
        """Test that the main function runs successfully."""
        mock_app_instance = Mock()
        mock_application.return_value = mock_app_instance
        
        from src.app import main
        main()
        
        # Verify that Application was instantiated and run was called
        mock_application.assert_called_once()
        mock_app_instance.run.assert_called_once()
    
    @patch('src.app.Application')
    @patch('sys.exit')
    def test_main_function_keyboard_interrupt(self, mock_exit, mock_application):
        """Test that the main function handles KeyboardInterrupt correctly."""
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = KeyboardInterrupt()
        mock_application.return_value = mock_app_instance
        
        from src.app import main
        main()
        
        # Verify that sys.exit was called with code 0
        mock_exit.assert_called_once_with(0)
    
    @patch('src.app.Application')
    @patch('sys.exit')
    def test_main_function_exception(self, mock_exit, mock_application):
        """Test that the main function handles exceptions correctly."""
        mock_app_instance = Mock()
        mock_app_instance.run.side_effect = Exception("Test error")
        mock_application.return_value = mock_app_instance
        
        from src.app import main
        main()
        
        # Verify that sys.exit was called with code 1
        mock_exit.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
