"""
Declarative menu configuration system.
Similar to WPF's XAML but in Python dictionaries.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Callable, Any


@dataclass
class MenuItemConfig:
    """Configuration for a single menu item."""
    label: str = ""
    command: Optional[Callable] = None
    accelerator: Optional[str] = None
    is_separator: bool = False
    submenu: Optional[List['MenuItemConfig']] = None
    enabled: bool = True
    visible: bool = True


@dataclass
class MenuConfig:
    """Complete menu bar configuration."""
    menus: List[MenuItemConfig]


class MenuBuilder:
    """Builds tkinter menus from configuration."""
    
    def __init__(self, root, command_handler):
        self.root = root
        self.command_handler = command_handler
        
    def build_menu(self, config: MenuConfig):
        """Build the complete menu bar from configuration."""
        import tkinter as tk
        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        for menu_config in config.menus:
            if menu_config.visible:
                menu = tk.Menu(menubar, tearoff=0)
                menubar.add_cascade(label=menu_config.label, menu=menu)
                self._build_menu_items(menu, menu_config.submenu or [])
        
        return menubar
    
    def _build_menu_items(self, menu, items: List[MenuItemConfig]):
        """Recursively build menu items."""
        for item in items:
            if not item.visible:
                continue
                
            if item.is_separator:
                menu.add_separator()
            elif item.submenu:
                # Submenu
                submenu = menu.add_cascade(label=item.label)
                self._build_menu_items(submenu, item.submenu)
            else:
                # Regular menu item
                command = None
                if item.command:
                    if isinstance(item.command, str):
                        # String reference to method name
                        command = getattr(self.command_handler, item.command, None)
                    else:
                        # Direct callable
                        command = item.command
                
                menu.add_command(
                    label=item.label,
                    command=command,
                    accelerator=item.accelerator,
                    state='normal' if item.enabled else 'disabled'
                )


def get_default_menu_config() -> MenuConfig:
    """Get the default menu configuration for the application."""
    return MenuConfig(menus=[
        MenuItemConfig(
            label="File",
            submenu=[
                MenuItemConfig(label="New", command="new_file", accelerator="Ctrl+N"),
                MenuItemConfig(label="Open", command="open_file", accelerator="Ctrl+O"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Save", command="save_file", accelerator="Ctrl+S"),
                MenuItemConfig(label="Save As", command="save_as_file", accelerator="Ctrl+Shift+S"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Exit", command="exit_app", accelerator="Ctrl+Q"),
            ]
        ),
        MenuItemConfig(
            label="Edit",
            submenu=[
                MenuItemConfig(label="Cut", command="cut", accelerator="Ctrl+X"),
                MenuItemConfig(label="Copy", command="copy", accelerator="Ctrl+C"),
                MenuItemConfig(label="Paste", command="paste", accelerator="Ctrl+V"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Select All", command="select_all", accelerator="Ctrl+A"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Find", command="find", accelerator="Ctrl+F"),
                MenuItemConfig(label="Replace", command="replace", accelerator="Ctrl+H"),
            ]
        ),
        MenuItemConfig(
            label="View",
            submenu=[
                MenuItemConfig(label="Toggle Theme", command="toggle_theme"),
                MenuItemConfig(label="Zoom In", command="zoom_in", accelerator="Ctrl+Plus"),
                MenuItemConfig(label="Zoom Out", command="zoom_out", accelerator="Ctrl+Minus"),
                MenuItemConfig(label="Reset Zoom", command="reset_zoom", accelerator="Ctrl+0"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Toggle Sidebar", command="toggle_sidebar"),
                MenuItemConfig(label="Toggle Status Bar", command="toggle_statusbar"),
            ]
        ),
        MenuItemConfig(
            label="Tools",
            submenu=[
                MenuItemConfig(label="Preferences", command="show_preferences"),
                MenuItemConfig(label="Export", command="export_data"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Plugin Manager", command="show_plugins"),
            ]
        ),
        MenuItemConfig(
            label="Help",
            submenu=[
                MenuItemConfig(label="User Guide", command="show_help"),
                MenuItemConfig(label="Keyboard Shortcuts", command="show_shortcuts"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Check for Updates", command="check_updates"),
                MenuItemConfig(label="About", command="show_about"),
            ]
        ),
    ])


def get_context_menu_config() -> MenuConfig:
    """Get context menu configuration for text area."""
    return MenuConfig(menus=[
        MenuItemConfig(
            label="Context",
            submenu=[
                MenuItemConfig(label="Cut", command="cut"),
                MenuItemConfig(label="Copy", command="copy"),
                MenuItemConfig(label="Paste", command="paste"),
                MenuItemConfig(is_separator=True),
                MenuItemConfig(label="Select All", command="select_all"),
            ]
        )
    ])
