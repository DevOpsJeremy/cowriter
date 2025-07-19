#!/usr/bin/env python3
"""
Main entry point for Cowriter.
This file provides compatibility for direct execution.
"""

import sys
from pathlib import Path

def main():
    """Main function to start the application."""
    try:
        # Add src directory to path for imports
        src_path = Path(__file__).parent / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
        
        from app import Application
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
