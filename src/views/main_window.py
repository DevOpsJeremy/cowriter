"""
Main window class for the application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import sv_ttk
from ..config import settings

class MainWindow:
    """Main application window."""
    
    def __init__(self, root):
        """Initialize the main window."""
        self.root = root
        self.logger = logging.getLogger(__name__)
        self.setup_menubar()
        self.setup_toolbar()
        self.setup_main_content()
        self.setup_statusbar()
        
    def setup_menubar(self):
        """Create and configure the menu bar."""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        
        # View menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        
        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
    def setup_toolbar(self):
        """Create and configure the toolbar."""
        self.toolbar_frame = ttk.Frame(self.root)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=(5, 0))
        
        # Toolbar buttons
        ttk.Button(self.toolbar_frame, text="New", command=self.new_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(self.toolbar_frame, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(self.toolbar_frame, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=(0, 5))
        
        # Separator
        ttk.Separator(self.toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Theme toggle button
        ttk.Button(self.toolbar_frame, text="Toggle Theme", command=self.toggle_theme).pack(side=tk.LEFT, padx=(0, 5))
        
    def setup_main_content(self):
        """Create and configure the main content area."""
        # Main container with paned window
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel
        self.left_frame = ttk.LabelFrame(self.main_container, text="Navigation", padding=10)
        self.main_container.add(self.left_frame, weight=1)
        
        # Treeview for navigation
        self.tree = ttk.Treeview(self.left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add some sample items
        self.tree.insert("", "end", text="Project", open=True)
        self.tree.insert("", "end", text="Documents")
        self.tree.insert("", "end", text="Settings")
        
        # Right panel - main content
        self.right_frame = ttk.LabelFrame(self.main_container, text="Content", padding=10)
        self.main_container.add(self.right_frame, weight=3)
        
        # Text area with scrollbar
        self.text_frame = ttk.Frame(self.right_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_area = tk.Text(self.text_frame, wrap=tk.WORD, undo=True)
        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add some placeholder text
        self.text_area.insert(tk.END, "Welcome to Cowriter!\\n\\n")
        self.text_area.insert(tk.END, "This is a modern desktop application built with:\\n")
        self.text_area.insert(tk.END, "• Python and tkinter\\n")
        self.text_area.insert(tk.END, "• Sun Valley theme (sv-ttk)\\n")
        self.text_area.insert(tk.END, "• Clean MVC architecture\\n\\n")
        self.text_area.insert(tk.END, "Start building your application logic here!")
        
    def setup_statusbar(self):
        """Create and configure the status bar."""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        
    def set_status(self, text):
        """Update the status bar text."""
        self.status_label.config(text=text)
        self.root.update_idletasks()
        
    def show_progress(self):
        """Show and start the progress bar."""
        self.progress.pack(side=tk.RIGHT, padx=(5, 0))
        self.progress.start()
        
    def hide_progress(self):
        """Hide and stop the progress bar."""
        self.progress.stop()
        self.progress.pack_forget()
        
    # Menu command handlers
    def new_file(self):
        """Handle new file command."""
        self.text_area.delete(1.0, tk.END)
        self.set_status("New file created")
        self.logger.info("New file created")
        
    def open_file(self):
        """Handle open file command."""
        filename = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
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
        if filename:
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
        
    def cut(self):
        """Handle cut command."""
        try:
            self.text_area.event_generate("<<Cut>>")
            self.set_status("Cut to clipboard")
        except:
            pass
            
    def copy(self):
        """Handle copy command."""
        try:
            self.text_area.event_generate("<<Copy>>")
            self.set_status("Copied to clipboard")
        except:
            pass
            
    def paste(self):
        """Handle paste command."""
        try:
            self.text_area.event_generate("<<Paste>>")
            self.set_status("Pasted from clipboard")
        except:
            pass
            
    def select_all(self):
        """Handle select all command."""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        
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

A modern Python desktop application built with tkinter and the Sun Valley theme."""
        
        messagebox.showinfo("About", about_text)
