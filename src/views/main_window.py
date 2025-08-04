"""
Main window class for the application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import sv_ttk
from ..config import settings
from .menu_config import MenuBuilder, get_default_menu_config
from .toolbar_config import ToolbarBuilder, get_default_toolbar_config
from .layout_config import LayoutBuilder, get_default_window_layout

class MainWindow:
    """Main application window."""
    
    def __init__(self, root):
        """Initialize the main window."""
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # Create builders
        self.menu_builder = MenuBuilder(root, self)
        self.toolbar_builder = ToolbarBuilder(root, self)
        self.layout_builder = LayoutBuilder(self)
        
        # Build UI from configuration
        self.setup_from_config()
        
    def setup_from_config(self):
        """Setup the entire UI from configuration."""
        # Get configurations
        window_layout = get_default_window_layout()
        menu_config = get_default_menu_config()
        toolbar_config = get_default_toolbar_config()
        
        # Build menu
        self.menubar = self.menu_builder.build_menu(menu_config)
        
        # Build main layout
        self.layout_builder.build_layout(self.root, window_layout.root_layout)
        
        # Build toolbar in its container
        toolbar_container = self.layout_builder.get_widget('toolbar_container')
        if toolbar_container:
            self.toolbar = self.toolbar_builder.build_toolbar(toolbar_config)
            self.toolbar.pack(fill=tk.X)
            # Reparent toolbar to the correct container
            self.toolbar.pack_forget()
            self.toolbar = self.toolbar_builder.build_toolbar(toolbar_config)
            self.toolbar.master = toolbar_container
            self.toolbar.pack(in_=toolbar_container, fill=tk.X)
        
        # Get references to important widgets
        self.text_area = self.layout_builder.get_widget('text_area')
        self.text_scrollbar = self.layout_builder.get_widget('text_scrollbar')
        self.navigation_tree = self.layout_builder.get_widget('navigation_tree')
        self.status_label = self.layout_builder.get_widget('status_label')
        self.progress_bar = self.layout_builder.get_widget('progress_bar')
        
        # Configure widgets that need special setup
        self.configure_widgets()
        self.setup_keyboard_shortcuts()
        self.populate_initial_content()
    
    def configure_widgets(self):
        """Configure widgets after creation."""
        # Configure text area scrollbar
        if self.text_area and self.text_scrollbar:
            self.text_scrollbar.config(command=self.text_area.yview)
            self.text_area.config(yscrollcommand=self.text_scrollbar.set)
        
        # Configure tree
        if self.navigation_tree:
            # Add some sample items
            self.navigation_tree.insert("", "end", text="Project", open=True)
            self.navigation_tree.insert("", "end", text="Documents")
            self.navigation_tree.insert("", "end", text="Settings")
        
        # Hide progress bar initially
        if self.progress_bar:
            self.progress_bar.pack_forget()
    
    def populate_initial_content(self):
        """Add initial content to the text area."""
        if self.text_area:
            self.text_area.insert(tk.END, "Welcome to Cowriter!\\n\\n")
            self.text_area.insert(tk.END, "This is a modern desktop application built with:\\n")
            self.text_area.insert(tk.END, "• Python and tkinter\\n")
            self.text_area.insert(tk.END, "• Sun Valley theme (sv-ttk)\\n")
            self.text_area.insert(tk.END, "• Declarative configuration system\\n")
            self.text_area.insert(tk.END, "• Clean separation of concerns\\n\\n")
            self.text_area.insert(tk.END, "The UI is now built from configuration objects,\\n")
            self.text_area.insert(tk.END, "similar to WPF's XAML approach!")
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        shortcuts = {
            '<Control-n>': self.new_file,
            '<Control-o>': self.open_file,
            '<Control-s>': self.save_file,
            '<Control-Shift-S>': self.save_as_file,
            '<Control-q>': self.exit_app,
            '<Control-x>': self.cut,
            '<Control-c>': self.copy,
            '<Control-v>': self.paste,
            '<Control-a>': self.select_all,
        }
        
        for key, command in shortcuts.items():
            self.root.bind(key, lambda e, cmd=command: cmd())
        
    def set_status(self, text):
        """Update the status bar text."""
        if self.status_label:
            self.status_label.config(text=text)
            self.root.update_idletasks()
        
    def show_progress(self):
        """Show and start the progress bar."""
        if self.progress_bar:
            self.progress_bar.pack(side=tk.RIGHT, padx=(5, 0))
            self.progress_bar.start()
        
    def hide_progress(self):
        """Hide and stop the progress bar."""
        if self.progress_bar:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
        
    # Menu command handlers
    def new_file(self):
        """Handle new file command."""
        if self.text_area:
            self.text_area.delete(1.0, tk.END)
        self.set_status("New file created")
        self.logger.info("New file created")
        
    def open_file(self):
        """Handle open file command."""
        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename and self.text_area:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                self.set_status(f"Opened: {filename}")
                self.logger.info(f"Opened file: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
                self.logger.error(f"Failed to open file {filename}: {e}")
                
    def save_file(self):
        """Handle save file command."""
        filename = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename and self.text_area:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.set_status(f"Saved: {filename}")
                self.logger.info(f"Saved file: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                self.logger.error(f"Failed to save file {filename}: {e}")
                
    def save_as_file(self):
        """Handle save as file command."""
        self.save_file()
    
    def exit_app(self):
        """Handle exit application command."""
        self.root.quit()
        
    def cut(self):
        """Handle cut command."""
        try:
            if self.text_area:
                self.text_area.event_generate("<<Cut>>")
            self.set_status("Cut to clipboard")
        except:
            pass
            
    def copy(self):
        """Handle copy command."""
        try:
            if self.text_area:
                self.text_area.event_generate("<<Copy>>")
            self.set_status("Copied to clipboard")
        except:
            pass
            
    def paste(self):
        """Handle paste command."""
        try:
            if self.text_area:
                self.text_area.event_generate("<<Paste>>")
            self.set_status("Pasted from clipboard")
        except:
            pass
            
    def select_all(self):
        """Handle select all command."""
        if self.text_area:
            self.text_area.tag_add(tk.SEL, "1.0", tk.END)
            self.text_area.mark_set(tk.INSERT, "1.0")
            self.text_area.see(tk.INSERT)
    
    # Additional command handlers for the extended menu
    def find(self):
        """Handle find command."""
        self.set_status("Find functionality not implemented yet")
    
    def replace(self):
        """Handle replace command."""
        self.set_status("Replace functionality not implemented yet")
    
    def zoom_in(self):
        """Handle zoom in command."""
        self.set_status("Zoom in not implemented yet")
    
    def zoom_out(self):
        """Handle zoom out command."""
        self.set_status("Zoom out not implemented yet")
    
    def reset_zoom(self):
        """Handle reset zoom command."""
        self.set_status("Reset zoom not implemented yet")
    
    def toggle_sidebar(self):
        """Handle toggle sidebar command."""
        self.set_status("Toggle sidebar not implemented yet")
    
    def toggle_statusbar(self):
        """Handle toggle status bar command."""
        self.set_status("Toggle status bar not implemented yet")
    
    def show_preferences(self):
        """Handle show preferences command."""
        self.set_status("Preferences dialog not implemented yet")
    
    def export_data(self):
        """Handle export data command."""
        self.set_status("Export functionality not implemented yet")
    
    def show_plugins(self):
        """Handle show plugins command."""
        self.set_status("Plugin manager not implemented yet")
    
    def show_help(self):
        """Handle show help command."""
        self.set_status("Help system not implemented yet")
    
    def show_shortcuts(self):
        """Handle show shortcuts command."""
        self.set_status("Keyboard shortcuts dialog not implemented yet")
    
    def check_updates(self):
        """Handle check updates command."""
        self.set_status("Update checker not implemented yet")
        
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        try:
            current_theme = sv_ttk.get_theme()
            new_theme = "light" if current_theme == "dark" else "dark"
            sv_ttk.set_theme(new_theme)
            self.set_status(f"Switched to {new_theme} theme")
            self.logger.info(f"Theme changed to {new_theme}")
        except Exception as e:
            messagebox.showerror("Theme Error", f"Failed to change theme: {e}")
            self.logger.error(f"Theme change failed: {e}")
        
    def show_about(self):
        """Show about dialog."""
        about_text = f"""{settings.APP_NAME}
Version {settings.APP_VERSION}
By {settings.APP_AUTHOR}

A modern Python desktop application built with:
• Declarative configuration system
• Clean separation of concerns
• WPF-inspired architecture"""
        
        messagebox.showinfo("About", about_text)
