#!/usr/bin/env python3
"""
DataSage AI - Easy Run Script

This script starts the DataSage AI application with optimal settings.
Use this as an alternative to the streamlit command for easier deployment.
"""

import subprocess
import sys
import os
import time

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'scipy', 'google.genai', 'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'google.genai':
                from google import genai
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    return missing_packages

def check_api_key():
    """Check if Gemini API key is available"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY found (starts with: {api_key[:10]}...)")
        return True
    else:
        print("⚠️  GEMINI_API_KEY not found")
        print("   Add your API key to environment variables or Replit Secrets")
        print("   Get a free key from: https://makersuite.google.com/app/apikey")
        return False

def install_missing_packages(packages):
    """Install missing packages"""
    if not packages:
        return True
    
    print(f"\n📦 Installing missing packages: {', '.join(packages)}")
    
    # Map package names to pip install names
    package_map = {
        'google.genai': 'google-genai'
    }
    
    pip_packages = [package_map.get(pkg, pkg) for pkg in packages]
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            *pip_packages
        ])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages")
        return False

def start_app():
    """Start the Streamlit application"""
    print("\n🚀 Starting DataSage AI...")
    print("   Opening in your browser at: http://localhost:5000")
    print("   Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '5000',
            '--server.address', '0.0.0.0',
            '--server.headless', 'false',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 DataSage AI stopped")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'streamlit'])
        start_app()

def main():
    """Main function to run DataSage AI"""
    print("🤖 DataSage AI - Startup Check")
    print("=" * 40)
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Missing {len(missing)} packages")
        install_choice = input("Install missing packages? (y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes']:
            if not install_missing_packages(missing):
                print("❌ Installation failed. Please install manually:")
                print("pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl")
                return
        else:
            print("❌ Cannot start without required packages")
            return
    
    # Check API key
    print("\n🔑 Checking API configuration...")
    has_api_key = check_api_key()
    
    if not has_api_key:
        print("\n⚠️  AI features will be limited without API key")
        continue_choice = input("Continue anyway? (y/n): ").lower().strip()
        
        if continue_choice not in ['y', 'yes']:
            print("👋 Setup your API key and try again")
            return
    
    print("\n✅ All checks passed!")
    time.sleep(1)
    
    # Start the application
    start_app()

if __name__ == "__main__":
    main()