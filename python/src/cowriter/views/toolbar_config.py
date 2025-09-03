"""
Declarative toolbar configuration system.
"""

from dataclasses import dataclass
from typing import List, Optional, Callable, Any
import tkinter as tk
from tkinter import ttk


@dataclass
class ToolbarItemConfig:
    """Configuration for a toolbar item."""
    type: str  # 'button', 'separator', 'label', 'entry', 'combobox'
    text: Optional[str] = None
    command: Optional[str] = None  # Method name on command handler
    tooltip: Optional[str] = None
    icon: Optional[str] = None
    width: Optional[int] = None
    enabled: bool = True
    visible: bool = True
    style: Optional[str] = None


@dataclass
class ToolbarConfig:
    """Complete toolbar configuration."""
    items: List[ToolbarItemConfig]
    orientation: str = 'horizontal'  # 'horizontal' or 'vertical'


class ToolbarBuilder:
    """Builds tkinter toolbars from configuration."""
    
    def __init__(self, parent, command_handler):
        self.parent = parent
        self.command_handler = command_handler
        
    def build_toolbar(self, config: ToolbarConfig) -> ttk.Frame:
        """Build toolbar from configuration."""
        toolbar_frame = ttk.Frame(self.parent)
        
        for item_config in config.items:
            if not item_config.visible:
                continue
                
            widget = self._create_toolbar_item(toolbar_frame, item_config)
            if widget:
                if config.orientation == 'horizontal':
                    widget.pack(side=tk.LEFT, padx=(0, 5))
                else:
                    widget.pack(side=tk.TOP, pady=(0, 5))
        
        return toolbar_frame
    
    def _create_toolbar_item(self, parent, config: ToolbarItemConfig):
        """Create a single toolbar item."""
        if config.type == 'button':
            command = None
            if config.command:
                command = getattr(self.command_handler, config.command, None)
            
            button = ttk.Button(
                parent,
                text=config.text,
                command=command,
                width=config.width,
                style=config.style
            )
            
            if config.tooltip:
                self._add_tooltip(button, config.tooltip)
            
            if not config.enabled:
                button.configure(state='disabled')
                
            return button
            
        elif config.type == 'separator':
            if parent.winfo_class() == 'Ttk::Frame':
                # For horizontal toolbar
                return ttk.Separator(parent, orient=tk.VERTICAL)
            else:
                return ttk.Separator(parent, orient=tk.HORIZONTAL)
                
        elif config.type == 'label':
            return ttk.Label(parent, text=config.text, style=config.style)
            
        elif config.type == 'entry':
            entry = ttk.Entry(parent, width=config.width, style=config.style)
            if config.tooltip:
                self._add_tooltip(entry, config.tooltip)
            return entry
            
        elif config.type == 'combobox':
            combo = ttk.Combobox(parent, width=config.width, style=config.style)
            if config.tooltip:
                self._add_tooltip(combo, config.tooltip)
            return combo
        
        return None
    
    def _add_tooltip(self, widget, text):
        """Add tooltip to widget (simple implementation)."""
        def on_enter(event):
            # You could implement a proper tooltip here
            pass
        def on_leave(event):
            pass
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)


def get_default_toolbar_config() -> ToolbarConfig:
    """Get the default toolbar configuration."""
    return ToolbarConfig(items=[
        ToolbarItemConfig(
            type='button',
            text='New',
            command='new_file',
            tooltip='Create a new file (Ctrl+N)'
        ),
        ToolbarItemConfig(
            type='button',
            text='Open',
            command='open_file',
            tooltip='Open an existing file (Ctrl+O)'
        ),
        ToolbarItemConfig(
            type='button',
            text='Save',
            command='save_file',
            tooltip='Save the current file (Ctrl+S)'
        ),
        ToolbarItemConfig(type='separator'),
        ToolbarItemConfig(
            type='button',
            text='Cut',
            command='cut',
            tooltip='Cut selected text (Ctrl+X)'
        ),
        ToolbarItemConfig(
            type='button',
            text='Copy',
            command='copy',
            tooltip='Copy selected text (Ctrl+C)'
        ),
        ToolbarItemConfig(
            type='button',
            text='Paste',
            command='paste',
            tooltip='Paste from clipboard (Ctrl+V)'
        ),
        ToolbarItemConfig(type='separator'),
        ToolbarItemConfig(
            type='button',
            text='Theme',
            command='toggle_theme',
            tooltip='Toggle between light and dark theme'
        ),
        ToolbarItemConfig(type='separator'),
        ToolbarItemConfig(
            type='label',
            text='Search:'
        ),
        ToolbarItemConfig(
            type='entry',
            width=20,
            tooltip='Enter search terms'
        ),
    ])
