# Cowriter

A modern Windows desktop application built with Python and tkinter, featuring the Sun Valley theme for a contemporary look.

## Features

- Modern Sun Valley theme (sv-ttk)
- Clean MVC architecture
- Configurable settings
- Error handling and logging
- Professional Windows-style interface

## Setup

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Project Structure

```
cowriter/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── pyproject.toml       # Project configuration
├── README.md           # This file
├── .gitignore          # Git ignore rules
├── src/                # Source code package
│   ├── __init__.py
│   ├── __main__.py     # Package entry point
│   ├── app.py          # Main application class
│   ├── config/         # Application configuration
│   │   └── settings.py
│   ├── models/         # Data models
│   ├── views/          # UI components
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── dialogs/
│   ├── controllers/    # Business logic
│   └── assets/         # Images, icons, etc.
└── tests/              # Unit tests
```

## Requirements

- Python 3.7+
- tkinter (included with Python)
- sv-ttk (Sun Valley theme)

## Development

The application follows an MVC pattern:
- **Models**: Data handling and business logic
- **Views**: UI components and layout
- **Controllers**: Event handling and coordination

## Building for Distribution

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --windowed --onefile main.py
```
