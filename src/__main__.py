#!/usr/bin/env python3
"""
Main entry point for Cowriter when run as a package.
"""

import sys
import os

from .app import Application

def main():
    """Main function to start the application."""
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
