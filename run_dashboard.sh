#!/bin/bash
# Inventory Intelligence Dashboard Launcher for Mac/Linux
# Run this file to start the dashboard

echo "========================================"
echo " Inventory Intelligence Dashboard"
echo " Starting..."
echo "========================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run installation first."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "ERROR: Streamlit not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install altair==4.2.2
fi

# Start the dashboard
echo ""
echo "Dashboard starting..."
echo "Open your browser and go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run app_tally.py
