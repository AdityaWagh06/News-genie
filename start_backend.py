#!/usr/bin/env python3
"""
NewsGenie Backend Startup Script
This script starts the FastAPI backend server with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the NewsGenie backend server"""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    app_dir = project_root / "app"
    
    # Check if we're in the right directory
    if not app_dir.exists():
        print("Error: app directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Stay in project root directory
    os.chdir(project_root)
    
    # Check if .env file exists, create if not
    env_file = project_root / ".env"
    if not env_file.exists():
        print("Creating .env file with default configuration...")
        with open(env_file, "w") as f:
            f.write("# NewsGenie Environment Variables\n")
            f.write("# Get your free API key at https://newsapi.org\n")
            f.write("NEWS_API_KEY=your_news_api_key_here\n")
        print("Created .env file. Please add your NewsAPI key to continue.")
    
    print("Starting NewsGenie Backend Server...")
    print("API Documentation will be available at:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server.\n")
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 