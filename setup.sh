#!/bin/bash

# AVAnA Setup Script - Android Vulnerability Analysis Framework
# This script sets up the environment and starts the application

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Android Vulnerability Static Analysis Framework (AVAnA)      ║"
echo "║                    Setup Script v1.0                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version detected: $python_version"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "• Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
    else
        echo "✗ Error creating virtual environment"
        exit 1
    fi
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv
echo "• Activating virtual environment..."
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment activated"
else
    echo "✗ Error activating virtual environment"
    exit 1
fi

# Install/update pip
echo "• Updating pip..."
pip install --upgrade pip -q
echo "✓ pip updated"

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "• Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✓ All dependencies installed successfully"
    else
        echo "✗ Error installing dependencies"
        exit 1
    fi
else
    echo "✗ requirements.txt not found"
    exit 1
fi

# Create necessary directories
echo "• Creating necessary directories..."
mkdir -p uploads logs
echo "✓ Directories created"

# Check if port 5000 is available
echo "• Checking if port 5000 is available..."
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠ Port 5000 is already in use"
    echo "  Please close the application using this port or edit the PORT in run.py"
    exit 1
else
    echo "✓ Port 5000 is available"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  Setup Complete! 🎉                           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Run the application: python3 run.py"
echo "  2. Open browser: http://localhost:5000"
echo "  3. Upload your APK to analyze"
echo ""
echo "For more information, see:"
echo "  • README.md - Full documentation"
echo "  • QUICKSTART.md - Quick start guide"
echo ""

# Optional: Start the application automatically
read -p "Would you like to start the application now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting AVAnA..."
    python3 run.py
else
    echo "You can start the application later with: python3 run.py"
    echo "Remember to activate the virtual environment first:"
    echo "  source venv/bin/activate"
fi
