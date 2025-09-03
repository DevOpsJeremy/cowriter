"""
Main application class that coordinates the entire application.
"""

import tkinter as tk
import logging
from pathlib import Path
import sv_ttk
from .config import settings
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
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "app.log"
        
        logging.basicConfig(
            level=getattr(logging, settings.LOG_LEVEL),
            format=settings.LOG_FORMAT,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file, encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        
    def setup_root_window(self):
        """Configure the root window."""
        self.root.title(settings.WINDOW_TITLE)
        self.root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
        self.root.minsize(settings.WINDOW_MIN_WIDTH, settings.WINDOW_MIN_HEIGHT)
        
        # Set application icon if available
        self.set_icon()
        
        # Center the window on screen
        self.center_window()
        
        # Configure the window closing behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def set_icon(self):
        """Set application icon if available."""
        icon_path = Path(settings.ASSETS_DIR) / "icon.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except Exception as e:
                self.logger.warning(f"Could not set icon: {e}")
        
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
            sv_ttk.set_theme(settings.THEME)
            self.logger.info(f"Applied {settings.THEME} theme successfully")
        except Exception as e:
            self.logger.error(f"Failed to apply theme: {e}")
            raise
            
    def on_closing(self):
        """Handle application closing."""
        self.logger.info("Application closing")
        self.root.quit()
        self.root.destroy()
        
    def run(self):
        """Start the application main loop."""
        print("Something")
        self.logger.info("Something")
        try:
            self.logger.info("Starting application main loop")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            raise
