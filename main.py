#!/usr/bin/env python3
"""
JScaner - Main Application Entry Point

This application reconstructs 3D objects from photographs taken against a reference grid.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Check for Open3D availability and warn user if not available
try:
    import open3d
    print("✓ Open3D available - full 3D reconstruction features enabled")
except ImportError:
    print("⚠ Open3D not available for Python 3.14 - using fallback reconstruction methods")
    print("  Some advanced 3D reconstruction features may be limited")
    print("  Consider using Python 3.11 or 3.12 for full Open3D support")

from gui.main_window import MainApplication

def main():
    """Launch the JScaner application."""
    try:
        app = MainApplication()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()