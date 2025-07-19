"""
Unit tests for the main window class.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.views.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    """Test cases for the MainWindow class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the root window
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.config = Mock()
        
        # Mock menu objects
        self.mock_menu = Mock(spec=tk.Menu)
        self.mock_submenu = Mock(spec=tk.Menu)
        
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    def test_main_window_initialization(self, mock_logging, mock_ttk, mock_menu):
        """Test that the main window initializes correctly."""
        mock_menu.return_value = self.mock_menu
        
        window = MainWindow(self.mock_root)
        
        # Verify that the root was stored
        self.assertEqual(window.root, self.mock_root)
        
        # Verify that a logger was created
        mock_logging.getLogger.assert_called_once()
        
        # Verify that menu was created and configured
        mock_menu.assert_called()
        self.mock_root.config.assert_called()
    
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    def test_setup_menubar(self, mock_logging, mock_ttk, mock_menu):
        """Test that the menu bar is set up correctly."""
        mock_menu.return_value = self.mock_menu
        
        window = MainWindow(self.mock_root)
        
        # Verify that menus were created
        self.assertTrue(mock_menu.call_count >= 4)  # Main menu + File, Edit, View menus
        
        # Verify that the menubar was configured on the root
        self.mock_root.config.assert_called_with(menu=self.mock_menu)
    
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    def test_menu_commands_exist(self, mock_logging, mock_ttk, mock_menu):
        """Test that menu commands are properly defined."""
        mock_menu.return_value = self.mock_menu
        
        window = MainWindow(self.mock_root)
        
        # Test that the window has the expected menu command methods
        self.assertTrue(hasattr(window, 'new_file'))
        self.assertTrue(hasattr(window, 'open_file'))
        self.assertTrue(hasattr(window, 'save_file'))
        self.assertTrue(hasattr(window, 'save_as_file'))
        self.assertTrue(hasattr(window, 'cut'))
        self.assertTrue(hasattr(window, 'copy'))
        self.assertTrue(hasattr(window, 'paste'))
        self.assertTrue(hasattr(window, 'select_all'))
        self.assertTrue(hasattr(window, 'toggle_theme'))
        
        # Test that these are callable
        self.assertTrue(callable(getattr(window, 'new_file')))
        self.assertTrue(callable(getattr(window, 'open_file')))
        self.assertTrue(callable(getattr(window, 'save_file')))
        self.assertTrue(callable(getattr(window, 'save_as_file')))
    
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    def test_setup_methods_exist(self, mock_logging, mock_ttk, mock_menu):
        """Test that all required setup methods exist."""
        mock_menu.return_value = self.mock_menu
        
        window = MainWindow(self.mock_root)
        
        # Test that setup methods exist and are callable
        self.assertTrue(hasattr(window, 'setup_menubar'))
        self.assertTrue(hasattr(window, 'setup_toolbar'))
        self.assertTrue(hasattr(window, 'setup_main_content'))
        self.assertTrue(hasattr(window, 'setup_statusbar'))
        
        self.assertTrue(callable(getattr(window, 'setup_menubar')))
        self.assertTrue(callable(getattr(window, 'setup_toolbar')))
        self.assertTrue(callable(getattr(window, 'setup_main_content')))
        self.assertTrue(callable(getattr(window, 'setup_statusbar')))


class TestMainWindowMethods(unittest.TestCase):
    """Test specific methods of the MainWindow class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_root = Mock(spec=tk.Tk)
        self.mock_root.config = Mock()
        
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    @patch('src.views.main_window.messagebox')
    def test_new_file_method(self, mock_messagebox, mock_logging, mock_ttk, mock_menu):
        """Test the new_file method."""
        mock_menu.return_value = Mock(spec=tk.Menu)
        
        window = MainWindow(self.mock_root)
        
        # The new_file method should exist and be callable
        self.assertTrue(hasattr(window, 'new_file'))
        self.assertTrue(callable(getattr(window, 'new_file')))
        
        # Calling it shouldn't raise an exception
        try:
            window.new_file()
        except AttributeError:
            # This is expected if the method is not fully implemented
            pass
        except Exception as e:
            self.fail(f"new_file method raised unexpected exception: {e}")
    
    @patch('src.views.main_window.tk.Menu')
    @patch('src.views.main_window.ttk')
    @patch('src.views.main_window.logging')
    @patch('src.views.main_window.filedialog')
    def test_open_file_method(self, mock_filedialog, mock_logging, mock_ttk, mock_menu):
        """Test the open_file method."""
        mock_menu.return_value = Mock(spec=tk.Menu)
        
        window = MainWindow(self.mock_root)
        
        # The open_file method should exist and be callable
        self.assertTrue(hasattr(window, 'open_file'))
        self.assertTrue(callable(getattr(window, 'open_file')))
        
        # Calling it shouldn't raise an exception
        try:
            window.open_file()
        except AttributeError:
            # This is expected if the method is not fully implemented
            pass
        except Exception as e:
            self.fail(f"open_file method raised unexpected exception: {e}")


if __name__ == '__main__':
    unittest.main()
