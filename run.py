#!/usr/bin/env python3
"""
Main entry point for the Android Vulnerability Analysis Framework
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Android Vulnerability Analysis Framework (AVAnA)")
    print("=" * 60)
    print("\n✓ Starting server...")
    print("✓ Navigate to http://localhost:5001 in your browser")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
