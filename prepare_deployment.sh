#!/bin/bash
# Deployment Package Preparation Script
# Creates a clean package ready for client deployment

echo "========================================"
echo " StockSense - Deployment Package Creator"
echo "========================================"
echo ""

# Get version and date
VERSION=${1:-1.0}
DATE=$(date +%Y%m%d)
PACKAGE_NAME="StockSense_v${VERSION}_${DATE}"
DEPLOY_DIR="../${PACKAGE_NAME}"

echo "Creating deployment package: $PACKAGE_NAME"
echo ""

# Create deployment directory
if [ -d "$DEPLOY_DIR" ]; then
    echo "Warning: Deployment directory already exists. Removing..."
    rm -rf "$DEPLOY_DIR"
fi

mkdir -p "$DEPLOY_DIR"

echo "Step 1: Copying essential files..."

# Copy Python files
cp -r ai_engine "$DEPLOY_DIR/"
cp -r automation "$DEPLOY_DIR/"
cp -r config "$DEPLOY_DIR/"
cp -r dashboard "$DEPLOY_DIR/"
cp -r data_ingestion "$DEPLOY_DIR/"
cp -r insights "$DEPLOY_DIR/"
cp -r models "$DEPLOY_DIR/"
cp -r subscription "$DEPLOY_DIR/"
cp -r utils "$DEPLOY_DIR/"

# Copy main application file
cp app_tally.py "$DEPLOY_DIR/"

# Copy installation and run scripts
cp install.sh "$DEPLOY_DIR/"
cp install.bat "$DEPLOY_DIR/"
cp run_dashboard.sh "$DEPLOY_DIR/"
cp run_dashboard.bat "$DEPLOY_DIR/"

# Copy requirements
cp requirements.txt "$DEPLOY_DIR/"

# Copy environment example (NOT .env with real keys!)
cp .env.example "$DEPLOY_DIR/"

# Copy documentation
cp README.md "$DEPLOY_DIR/"
cp CLIENT_INSTALL_GUIDE.md "$DEPLOY_DIR/"
cp INSTALLATION.md "$DEPLOY_DIR/"
cp QUICK_START.md "$DEPLOY_DIR/"
cp DEPLOYMENT_CHECKLIST.md "$DEPLOY_DIR/"
cp FEATURES_IMPLEMENTED.md "$DEPLOY_DIR/"
cp SUBSCRIPTION_SETUP.md "$DEPLOY_DIR/" 2>/dev/null || true
cp PACKAGES_GUIDE.md "$DEPLOY_DIR/" 2>/dev/null || true

echo "Step 2: Creating empty directories..."

# Create empty directories for data and logs
mkdir -p "$DEPLOY_DIR/data"
mkdir -p "$DEPLOY_DIR/logs"

# Create .gitkeep files to preserve directory structure
touch "$DEPLOY_DIR/data/.gitkeep"
touch "$DEPLOY_DIR/logs/.gitkeep"

echo "Step 3: Cleaning up unnecessary files..."

# Remove Python cache files
find "$DEPLOY_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$DEPLOY_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$DEPLOY_DIR" -type f -name "*.pyo" -delete 2>/dev/null || true
find "$DEPLOY_DIR" -type f -name ".DS_Store" -delete 2>/dev/null || true

echo "Step 4: Making scripts executable..."

chmod +x "$DEPLOY_DIR/install.sh"
chmod +x "$DEPLOY_DIR/run_dashboard.sh"

echo "Step 5: Creating README for deployment..."

cat > "$DEPLOY_DIR/START_HERE.txt" << 'EOF'
========================================
  StockSense - AI Inventory Intelligence
========================================

QUICK START:

1. INSTALL:
   Windows: Double-click "install.bat"
   Mac/Linux: Run "./install.sh" in Terminal

2. RUN:
   Windows: Double-click "run_dashboard.bat"
   Mac/Linux: Run "./run_dashboard.sh"

3. ACCESS:
   Open browser to: http://localhost:8501

DOCUMENTATION:
- CLIENT_INSTALL_GUIDE.md - Simple installation guide
- INSTALLATION.md - Detailed installation instructions
- README.md - Application overview
- QUICK_START.md - How to use the application

REQUIREMENTS:
- Python 3.9 or higher
- 500 MB disk space
- Internet connection (for installation only)

SUPPORT:
Check documentation files for troubleshooting.

========================================
EOF

echo "Step 6: Creating version info..."

cat > "$DEPLOY_DIR/VERSION.txt" << EOF
StockSense Deployment Package
Version: $VERSION
Build Date: $(date +"%Y-%m-%d %H:%M:%S")
Package: $PACKAGE_NAME

Included Components:
- Core application (app_tally.py)
- AI Engine modules
- Data ingestion tools
- Dashboard interface
- Subscription management
- Documentation

Installation: See CLIENT_INSTALL_GUIDE.md
Support: See documentation files
EOF

echo "Step 7: Creating deployment package..."

cd ..
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME" -q

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo " Package Created Successfully!"
    echo "========================================"
    echo ""
    echo "Package Location: ../${PACKAGE_NAME}.zip"
    echo "Package Size: $(du -h "${PACKAGE_NAME}.zip" | cut -f1)"
    echo ""
    echo "Package Contents:"
    echo "  - Source code and modules"
    echo "  - Installation scripts"
    echo "  - Documentation"
    echo "  - Empty data and logs directories"
    echo ""
    echo "IMPORTANT:"
    echo "  ✓ Virtual environment (.venv) excluded"
    echo "  ✓ Cache files excluded"
    echo "  ✓ .env file excluded (only .env.example included)"
    echo "  ✓ Test data excluded"
    echo ""
    echo "Next Steps:"
    echo "  1. Copy ${PACKAGE_NAME}.zip to USB or send to client"
    echo "  2. Client extracts the ZIP file"
    echo "  3. Client runs install script"
    echo "  4. Follow DEPLOYMENT_CHECKLIST.md"
    echo ""

    # Ask if we should clean up the unzipped folder
    read -p "Remove unzipped deployment folder? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PACKAGE_NAME"
        echo "Unzipped folder removed. ZIP file preserved."
    else
        echo "Both ZIP and unzipped folder preserved."
    fi
else
    echo "ERROR: Failed to create ZIP package"
    exit 1
fi

echo ""
echo "Deployment package ready! 🚀"
echo ""
