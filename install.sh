#!/bin/bash
# Quick Installation Script for Mac/Linux

echo "========================================"
echo " Inventory Intelligence System"
echo " Installation Wizard"
echo "========================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found!"
    echo "Please install Python 3.9 or higher"
    echo ""
    echo "macOS: brew install python@3.9"
    echo "Ubuntu/Debian: sudo apt install python3.9 python3.9-venv python3-pip"
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Python found!"
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    read -p "Press Enter to exit..."
    exit 1
fi

# Install compatible altair
echo "Installing compatible Altair version..."
pip install altair==4.2.2

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Create data directories
mkdir -p data
mkdir -p logs

# Make run script executable
chmod +x run_dashboard.sh

echo ""
echo "========================================"
echo " Installation Complete!"
echo "========================================"
echo ""
echo "To start the dashboard, run:"
echo "   ./run_dashboard.sh"
echo ""
echo "Or run manually:"
echo "   source .venv/bin/activate"
echo "   streamlit run app_tally.py"
echo ""
