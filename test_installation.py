#!/usr/bin/env python3
"""
NewsGenie Installation Test Script
This script tests if all dependencies are properly installed and the system is ready to run.
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {e}")
        return False

def test_file_exists(file_path, description):
    """Test if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description}: File not found")
        return False

def main():
    """Run installation tests"""
    print("🧠 NewsGenie Installation Test")
    print("=" * 40)
    
    # Test Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python version: {python_version.major}.{python_version.minor}.{python_version.micro} (requires 3.8+)")
        return False
    
    print("\n📦 Testing Python Dependencies:")
    
    # Test core dependencies
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("requests", "Requests"),
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
        ("sklearn", "Scikit-learn"),
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("pydantic", "Pydantic"),
        ("python-dotenv", "Python-dotenv"),
        ("pytest", "Pytest"),
        ("httpx", "HTTPX"),
    ]
    
    all_passed = True
    for module, name in dependencies:
        if not test_import(module, name):
            all_passed = False
    
    print("\n📁 Testing Project Structure:")
    
    # Test project files
    files_to_test = [
        ("requirements.txt", "Requirements file"),
        ("app/main.py", "Main FastAPI app"),
        ("app/summarizer.py", "Summarizer module"),
        ("app/recommender.py", "Recommender module"),
        ("app/utils.py", "Utils module"),
        ("app/models.py", "Pydantic models"),
        ("tests/test_summarizer.py", "Summarizer tests"),
        ("tests/test_recommender.py", "Recommender tests"),
        ("tests/test_api.py", "API tests"),
        ("data/mock_users.json", "Mock data"),
        ("frontend/package.json", "Frontend package.json"),
        ("frontend/src/App.tsx", "React App component"),
    ]
    
    for file_path, description in files_to_test:
        if not test_file_exists(file_path, description):
            all_passed = False
    
    print("\n🔧 Testing Configuration:")
    
    # Test .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        with open(env_file, "r") as f:
            content = f.read()
            if "NEWS_API_KEY" in content:
                print("✅ NEWS_API_KEY configured")
            else:
                print("⚠️  NEWS_API_KEY not found in .env file")
    else:
        print("⚠️  .env file not found (will be created on first run)")
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! NewsGenie is ready to run.")
        print("\nNext steps:")
        print("1. Add your NewsAPI key to .env file")
        print("2. Run: python start_backend.py")
        print("3. In another terminal: cd frontend && npm install && npm start")
    else:
        print("❌ Some tests failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    main() 