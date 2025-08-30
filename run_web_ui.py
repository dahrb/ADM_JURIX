#!/usr/bin/env python3
"""
Startup script for the ADM Web UI
Run this script to start the modern web interface
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_socketio
        import pydot
        import pythonds
        print("✓ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("ADM Web UI - Modern Interface for Argumentation Decision Framework")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('web_ui.py'):
        print("✗ Error: web_ui.py not found in current directory")
        print("Please run this script from the ADM project directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling missing dependencies...")
        if not install_dependencies():
            print("✗ Failed to install dependencies. Please install manually:")
            print("  pip install -r requirements.txt")
            sys.exit(1)
    
    print("\nStarting ADM Web UI...")
    print("The interface will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the web UI
        from web_ui import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
