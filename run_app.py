#!/usr/bin/env python3
"""
Simple script to run both FastAPI backend and Streamlit frontend.
This makes it easier to start the entire application with one command.
"""


import subprocess
import sys
import time
import os
from threading import Thread

def run_fastapi():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FastAPI server failed to start: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 FastAPI server stopped by user")

def run_streamlit():
    """Run the Streamlit frontend server"""
    print("🎨 Starting Streamlit frontend server...")
    time.sleep(3)  # Give FastAPI time to start first
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit server failed to start: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit server stopped by user")

def check_prerequisites():
    """Check if all required files exist"""
    required_files = ["main.py", "finance_utils.py", "streamlit_app.py", "requirements.txt"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease make sure all files are in the current directory.")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your Alpha Vantage API key:")
        print("API_KEY=your_alpha_vantage_api_key_here")
        print()
        
        response = input("Continue anyway? (y/N): ").lower().strip()
        if response != 'y':
            print("Setup cancelled. Please create .env file first.")
            sys.exit(1)

def main():
    """Main function to coordinate the startup"""
    print("=" * 60)
    print("📈 Stock Performance Analyzer - Python Version")
    print("=" * 60)
    
    # Check prerequisites
    check_prerequisites()
    
    print("\n✅ All required files found!")
    print("\n🔧 Starting application servers...")
    print("   - FastAPI backend will run on: http://localhost:8000")
    print("   - Streamlit frontend will run on: http://localhost:8501")
    print("\n💡 Press Ctrl+C to stop both servers")
    print("-" * 60)
    
    try:
        # Start both servers in separate threads
        fastapi_thread = Thread(target=run_fastapi, daemon=True)
        streamlit_thread = Thread(target=run_streamlit, daemon=True)
        
        fastapi_thread.start()
        streamlit_thread.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        print("👋 Thanks for using Stock Performance Analyzer!")
        sys.exit(0)

if __name__ == "__main__":
    main() 
