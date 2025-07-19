"""
Main application class that coordinates the entire application.
"""

import tkinter as tk
import logging
import sv_ttk
from .config.settings import *
from .views.main_window import MainWindow

class Application:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.setup_logging()
        self.root = tk.Tk()
        self.setup_root_window()
        self.setup_theme()
        self.main_window = MainWindow(self.root)
        
    def setup_logging(self):
        """Setup application logging."""
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format=LOG_FORMAT,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
        
    def setup_root_window(self):
        """Configure the root window."""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Center the window on screen
        self.center_window()
        
        # Configure the window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_theme(self):
        """Apply the Sun Valley theme."""
        try:
            sv_ttk.set_theme(THEME)
            self.logger.info(f"Applied {THEME} theme successfully")
        except Exception as e:
            self.logger.error(f"Failed to apply theme: {e}")
            
    def on_closing(self):
        """Handle application closing."""
        self.logger.info("Application closing")
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Start the application main loop."""
        try:
            self.logger.info("Starting application main loop")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            raise

def main():
    """Entry point for the application when installed as a package."""
    import sys
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
