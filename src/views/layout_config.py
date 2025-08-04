"""
Declarative layout configuration system.
Similar to WPF's XAML layout system.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
import tkinter as tk
from tkinter import ttk


@dataclass
class LayoutConfig:
    """Base configuration for layout elements."""
    type: str
    name: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    padding: Optional[Union[int, tuple]] = None
    margin: Optional[Union[int, tuple]] = None
    fill: str = 'none'  # 'none', 'x', 'y', 'both'
    expand: bool = False
    anchor: str = 'nw'
    side: str = 'top'  # for pack geometry
    weight: int = 1  # for grid/paned windows
    visible: bool = True
    enabled: bool = True
    properties: Optional[Dict[str, Any]] = None
    children: Optional[List['LayoutConfig']] = None


@dataclass 
class WindowLayout:
    """Complete window layout configuration."""
    title: str
    geometry: str
    resizable: tuple = (True, True)
    root_layout: LayoutConfig = None


class LayoutBuilder:
    """Builds tkinter layouts from configuration."""
    
    def __init__(self, command_handler=None):
        self.command_handler = command_handler
        self.widgets = {}  # name -> widget mapping
    
    def build_layout(self, parent, config: LayoutConfig):
        """Build layout from configuration."""
        if not config.visible:
            return None
            
        widget = self._create_widget(parent, config)
        
        if config.name:
            self.widgets[config.name] = widget
            
        # Apply layout properties
        self._apply_layout_properties(widget, config)
        
        # Build children
        if config.children:
            for child_config in config.children:
                self.build_layout(widget, child_config)
                
        return widget
    
    def _create_widget(self, parent, config: LayoutConfig):
        """Create widget based on configuration type."""
        widget_type = config.type.lower()
        props = config.properties or {}
        
        if widget_type == 'frame':
            return ttk.Frame(parent, **props)
            
        elif widget_type == 'labelframe':
            return ttk.LabelFrame(parent, **props)
            
        elif widget_type == 'panedwindow':
            orient = props.get('orient', 'horizontal')
            if orient == 'horizontal':
                orient = tk.HORIZONTAL
            else:
                orient = tk.VERTICAL
            return ttk.PanedWindow(parent, orient=orient, **{k:v for k,v in props.items() if k != 'orient'})
            
        elif widget_type == 'notebook':
            return ttk.Notebook(parent, **props)
            
        elif widget_type == 'text':
            return tk.Text(parent, **props)
            
        elif widget_type == 'treeview':
            return ttk.Treeview(parent, **props)
            
        elif widget_type == 'scrollbar':
            return ttk.Scrollbar(parent, **props)
            
        elif widget_type == 'label':
            return ttk.Label(parent, **props)
            
        elif widget_type == 'button':
            command = props.get('command')
            if isinstance(command, str) and self.command_handler:
                props['command'] = getattr(self.command_handler, command, None)
            return ttk.Button(parent, **props)
            
        elif widget_type == 'entry':
            return ttk.Entry(parent, **props)
            
        elif widget_type == 'combobox':
            return ttk.Combobox(parent, **props)
            
        elif widget_type == 'progressbar':
            return ttk.Progressbar(parent, **props)
            
        else:
            # Fallback to Frame
            return ttk.Frame(parent)
    
    def _apply_layout_properties(self, widget, config: LayoutConfig):
        """Apply layout properties to widget."""
        pack_options = {}
        
        if config.fill != 'none':
            pack_options['fill'] = getattr(tk, config.fill.upper())
        if config.expand:
            pack_options['expand'] = True
        if config.side:
            pack_options['side'] = getattr(tk, config.side.upper())
        if config.anchor:
            pack_options['anchor'] = config.anchor
        if config.padding:
            if isinstance(config.padding, int):
                pack_options['padx'] = pack_options['pady'] = config.padding
            else:
                pack_options['padx'] = config.padding[0] if len(config.padding) > 0 else 0
                pack_options['pady'] = config.padding[1] if len(config.padding) > 1 else 0
        
        # Handle PanedWindow children differently
        parent = widget.master
        if isinstance(parent, ttk.PanedWindow):
            parent.add(widget, weight=config.weight)
        else:
            widget.pack(**pack_options)
    
    def get_widget(self, name: str):
        """Get widget by name."""
        return self.widgets.get(name)


def get_default_window_layout() -> WindowLayout:
    """Get the default window layout configuration."""
    return WindowLayout(
        title="Cowriter",
        geometry="800x600",
        root_layout=LayoutConfig(
            type='frame',
            name='root',
            fill='both',
            expand=True,
            children=[
                # Toolbar
                LayoutConfig(
                    type='frame',
                    name='toolbar_container',
                    fill='x',
                    side='top',
                    padding=(5, 5),
                ),
                
                # Main content area
                LayoutConfig(
                    type='panedwindow',
                    name='main_paned',
                    fill='both',
                    expand=True,
                    side='top',
                    padding=5,
                    properties={'orient': 'horizontal'},
                    children=[
                        # Left panel
                        LayoutConfig(
                            type='labelframe',
                            name='left_panel',
                            weight=1,
                            properties={
                                'text': 'Navigation',
                                'padding': 10
                            },
                            children=[
                                LayoutConfig(
                                    type='treeview',
                                    name='navigation_tree',
                                    fill='both',
                                    expand=True,
                                )
                            ]
                        ),
                        
                        # Right panel
                        LayoutConfig(
                            type='labelframe',
                            name='right_panel',
                            weight=3,
                            properties={
                                'text': 'Content',
                                'padding': 10
                            },
                            children=[
                                LayoutConfig(
                                    type='frame',
                                    name='text_container',
                                    fill='both',
                                    expand=True,
                                    children=[
                                        LayoutConfig(
                                            type='text',
                                            name='text_area',
                                            fill='both',
                                            expand=True,
                                            side='left',
                                            properties={
                                                'wrap': 'word',
                                                'undo': True
                                            }
                                        ),
                                        LayoutConfig(
                                            type='scrollbar',
                                            name='text_scrollbar',
                                            fill='y',
                                            side='right',
                                            properties={
                                                'orient': 'vertical'
                                            }
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Status bar
                LayoutConfig(
                    type='frame',
                    name='status_container',
                    fill='x',
                    side='bottom',
                    padding=(5, 5),
                    children=[
                        LayoutConfig(
                            type='label',
                            name='status_label',
                            side='left',
                            properties={'text': 'Ready'}
                        ),
                        LayoutConfig(
                            type='progressbar',
                            name='progress_bar',
                            side='right',
                            properties={
                                'mode': 'indeterminate',
                                'length': 200
                            }
                        )
                    ]
                )
            ]
        )
    )
