# Cowriter

A modern cross-platform desktop application built with Python and tkinter, featuring the Sun Valley theme for a contemporary look. Optimized for Windows deployment.

## Features

- Modern Sun Valley theme (sv-ttk) with fallback to default theme
- Clean MVC architecture
- Configurable settings
- Comprehensive error handling and logging
- Professional Windows-style interface
- Cross-platform compatibility (Windows, Linux, macOS)

## Windows Quick Start

1. **Download** or clone this project
2. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```
3. **Run** the application:
   ```cmd
   python -m src
   ```

## Manual Setup

### Prerequisites
- Python 3.8+ (Download from [python.org](https://python.org))
- tkinter (included with Python on Windows)

### Installation Steps

1. Clone or download this project:
   ```bash
   git clone https://github.com/DevOpsJeremy/cowriter.git
   cd cowriter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python -m src
   ```

## Alternative Installation (As Package)

```bash
pip install -e .
cowriter
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

- **Python 3.8+** (Download from [python.org](https://python.org))
- **tkinter** (included with Python on Windows)
- **sv-ttk** (Sun Valley theme - automatically installed)

## Building Standalone Executable

### Automated CI/CD (Recommended)
Push code to GitHub and the Actions workflow will automatically:
- Run tests on multiple Python versions
- Build Windows executable on Windows runner
- Create releases with attached executables for tagged versions

### Local Development Build (Windows)
For local testing and development:

```bash
# Use the provided script
build_windows.bat

# Or manually:
pip install pyinstaller
pyinstaller --windowed --onefile --name Cowriter src\__main__.py

# With icon (if you have icon.ico):
pyinstaller --windowed --onefile --name Cowriter --icon=src\assets\icon.ico src\__main__.py
```

The executable will be created in the `dist/` folder.

### Release Process
1. Update version in `src/__init__.py` and `src/config/settings.py`
2. Commit changes
3. Create and push a version tag: `git tag v1.0.0 && git push origin v1.0.0`
4. GitHub Actions will automatically create a release with the Windows executable

## Development

The application follows an MVC pattern:
- **Models**: Data handling and business logic (`src/models/`)
- **Views**: UI components and layout (`src/views/`)
- **Controllers**: Event handling and coordination (`src/controllers/`)
- **Config**: Application settings (`src/config/`)

## Troubleshooting

### Common Issues

1. **"tkinter not found"** (Linux/macOS):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # macOS
   brew install python-tk
   ```

2. **"sv-ttk not found"**:
   ```bash
   pip install sv-ttk
   ```

3. **Permission errors with logs**:
   - The app creates a `logs/` directory automatically
   - Ensure write permissions in the application directory

### Windows-Specific Notes
- Use `python` command (not `python3`)
- Make sure Python is added to PATH during installation
- Run Command Prompt as Administrator if you encounter permission issues
