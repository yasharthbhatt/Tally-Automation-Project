# 📦 Installation Guide - Inventory Intelligence System

## Complete Setup Instructions for Any System

---

## 📋 System Requirements

### Minimum Requirements:
- **OS:** Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM:** 4 GB (8 GB recommended)
- **Storage:** 500 MB free space
- **Python:** 3.9 or higher
- **Internet:** Required for initial installation only

### Recommended:
- **RAM:** 8 GB or more
- **Storage:** 1 GB free space
- **Processor:** Multi-core processor for faster analysis

---

## 🚀 Quick Installation (All Platforms)

### Step 1: Install Python

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

**If not installed:**

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer
- ✅ **Check "Add Python to PATH"**
- Click "Install Now"

**macOS:**
```bash
# Using Homebrew
brew install python@3.9

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
```

---

### Step 2: Get the Application

**Option A: Download ZIP (Easiest)**
1. Download the project folder
2. Extract to desired location (e.g., `C:\InventoryIntelligence` or `/home/user/InventoryIntelligence`)

**Option B: Git Clone (If you have Git)**
```bash
git clone <repository-url>
cd AIProjectForCustomerIntelligence
```

---

### Step 3: Install Dependencies

**Open Terminal/Command Prompt in the project folder**

**Windows:**
```cmd
# Navigate to folder
cd C:\path\to\AIProjectForCustomerIntelligence

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install compatible altair
pip install altair==4.2.2
```

**macOS/Linux:**
```bash
# Navigate to folder
cd /path/to/AIProjectForCustomerIntelligence

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install compatible altair
pip install altair==4.2.2
```

---

### Step 4: Initial Configuration (Optional)

**Create environment file:**
```bash
cp .env.example .env
```

**Edit `.env` file (optional):**
```
LOW_STOCK_THRESHOLD=10
REORDER_POINT_MULTIPLIER=1.5
```

---

### Step 5: Run the Application

**Windows:**
```cmd
# Make sure virtual environment is activated
.venv\Scripts\activate

# Run the dashboard
streamlit run app_tally.py
```

**macOS/Linux:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Run the dashboard
streamlit run app_tally.py
```

**The dashboard will open automatically at:** `http://localhost:8501`

If it doesn't open automatically, copy the URL from terminal and paste in your browser.

---

## 🖥️ Platform-Specific Instructions

### Windows Installation (Detailed)

**Step-by-Step:**

1. **Download Python:**
   - Go to python.org/downloads
   - Download Python 3.9+ installer
   - Run installer
   - ✅ Check "Add Python to PATH"
   - Click "Install Now"

2. **Verify Installation:**
   ```cmd
   python --version
   pip --version
   ```

3. **Download Application:**
   - Download ZIP file
   - Extract to `C:\InventoryIntelligence`

4. **Open Command Prompt:**
   - Press `Win + R`
   - Type `cmd`
   - Press Enter

5. **Navigate to Folder:**
   ```cmd
   cd C:\InventoryIntelligence
   ```

6. **Setup:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pip install altair==4.2.2
   ```

7. **Run:**
   ```cmd
   streamlit run app_tally.py
   ```

8. **Create Desktop Shortcut (Optional):**
   - Create new file: `run_dashboard.bat`
   - Add content:
   ```batch
   @echo off
   cd C:\InventoryIntelligence
   call .venv\Scripts\activate
   streamlit run app_tally.py
   pause
   ```
   - Double-click to run!

---

### macOS Installation (Detailed)

**Step-by-Step:**

1. **Install Homebrew (if not installed):**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python:**
   ```bash
   brew install python@3.9
   ```

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

4. **Download Application:**
   - Download ZIP
   - Extract to `/Users/yourusername/InventoryIntelligence`

5. **Open Terminal:**
   - Press `Cmd + Space`
   - Type "Terminal"
   - Press Enter

6. **Navigate to Folder:**
   ```bash
   cd ~/InventoryIntelligence
   ```

7. **Setup:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install altair==4.2.2
   ```

8. **Run:**
   ```bash
   streamlit run app_tally.py
   ```

9. **Create Launcher Script (Optional):**
   - Create file: `run_dashboard.sh`
   - Add content:
   ```bash
   #!/bin/bash
   cd ~/InventoryIntelligence
   source .venv/bin/activate
   streamlit run app_tally.py
   ```
   - Make executable: `chmod +x run_dashboard.sh`
   - Double-click to run!

---

### Linux Installation (Ubuntu/Debian)

**Step-by-Step:**

1. **Update System:**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Install Python:**
   ```bash
   sudo apt install python3.9 python3.9-venv python3-pip
   ```

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

4. **Download Application:**
   ```bash
   cd ~
   # Download and extract, or use git clone
   ```

5. **Navigate to Folder:**
   ```bash
   cd ~/AIProjectForCustomerIntelligence
   ```

6. **Setup:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install altair==4.2.2
   ```

7. **Run:**
   ```bash
   streamlit run app_tally.py
   ```

8. **Create Desktop Launcher (Optional):**
   - Create file: `~/Desktop/InventoryIntelligence.desktop`
   - Add content:
   ```ini
   [Desktop Entry]
   Type=Application
   Name=Inventory Intelligence
   Exec=/home/yourusername/AIProjectForCustomerIntelligence/run_dashboard.sh
   Icon=utilities-terminal
   Terminal=true
   ```

---

## 🌐 Network Installation (Share Across Office)

### Setup on Server Computer:

1. **Install as above on one computer**

2. **Run with network access:**
   ```bash
   streamlit run app_tally.py --server.address 0.0.0.0 --server.port 8501
   ```

3. **Find server IP address:**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `ip addr`
   - Look for IP like `192.168.1.100`

4. **Access from other computers:**
   - Open browser
   - Go to: `http://192.168.1.100:8501`
   - Replace with your server's IP

### Security Note:
- Only share on trusted local networks
- Don't expose to internet without proper security

---

## 🔄 Daily Usage

### Starting the Application:

**Windows:**
```cmd
cd C:\InventoryIntelligence
.venv\Scripts\activate
streamlit run app_tally.py
```

**macOS/Linux:**
```bash
cd ~/InventoryIntelligence
source .venv/bin/activate
streamlit run app_tally.py
```

### Stopping the Application:
- Press `Ctrl + C` in the terminal
- Or close the terminal window

---

## 📤 Preparing Your Data

Before first use:

1. **Export from Tally:**
   - Product-wise reports (Price Fluctuation, Customer Adoption, Stock Summary)
   - Customer ledger report
   - Save as Excel files

2. **File Format:**
   - `product_wise_reports.xlsx` with sheets:
     - Price Fluctuation
     - Customer Adoption
     - Stock Summary
   - `sample_tally_customer_report.xlsx` with sheet:
     - Customer Ledger Report

3. **Upload in Dashboard:**
   - Open dashboard
   - Use sidebar to upload files
   - Click "Process & Analyze"

---

## 🔧 Troubleshooting

### Python Not Found
**Windows:**
- Reinstall Python
- Check "Add Python to PATH"

**Mac/Linux:**
```bash
sudo apt install python3.9  # Linux
brew install python@3.9     # Mac
```

### Permission Denied
**Mac/Linux:**
```bash
chmod +x run_dashboard.sh
```

### Port Already in Use
```bash
# Use different port
streamlit run app_tally.py --server.port 8502
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Streamlit Version Issues
```bash
pip uninstall streamlit altair
pip install streamlit altair==4.2.2
```

### Virtual Environment Not Activating
**Windows:**
```cmd
# Try this command
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🔄 Updating the Application

### Get Latest Version:
1. Download new version
2. Extract to same location
3. Activate virtual environment
4. Update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Preserve Your Data:
- Your data in `data/` folder is safe
- Configuration in `.env` is preserved
- Just update the code files

---

## 💾 Backup & Recovery

### What to Backup:
```
data/                    # All your business data
.env                     # Your configuration
logs/                    # Optional: Analysis history
```

### Backup Command:
**Windows:**
```cmd
xcopy data data_backup_20260327 /E /I
```

**Mac/Linux:**
```bash
cp -r data/ data_backup_$(date +%Y%m%d)/
```

### Recovery:
- Just copy `data/` folder back
- Reinstall application
- Your data is restored!

---

## 🚀 Auto-Start on Boot (Optional)

### Windows:
1. Create shortcut of `run_dashboard.bat`
2. Press `Win + R`
3. Type `shell:startup`
4. Paste shortcut there

### macOS:
1. System Preferences → Users & Groups → Login Items
2. Add `run_dashboard.sh`

### Linux (systemd):
Create `/etc/systemd/system/inventory-intelligence.service`:
```ini
[Unit]
Description=Inventory Intelligence Dashboard
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/home/yourusername/InventoryIntelligence
ExecStart=/home/yourusername/InventoryIntelligence/.venv/bin/streamlit run app_tally.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable inventory-intelligence
sudo systemctl start inventory-intelligence
```

---

## 📞 Installation Support

### Common Issues:

| Issue | Solution |
|-------|----------|
| Python not found | Add Python to PATH |
| pip not found | `python -m pip` instead |
| Permission denied | Run as administrator (Windows) or use `sudo` (Linux/Mac) |
| Port in use | Use `--server.port 8502` |
| Module errors | `pip install -r requirements.txt --force-reinstall` |

### Need Help?
- Check `README.md` for more details
- Check `QUICK_START.md` for usage guide
- Review error messages in terminal

---

## ✅ Installation Checklist

- [ ] Python 3.9+ installed
- [ ] Project folder extracted
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Altair 4.2.2 installed
- [ ] Application runs successfully
- [ ] Dashboard opens in browser
- [ ] Can upload Tally files
- [ ] Analysis completes successfully

---

## 🎉 You're Ready!

Once installed:
1. Run the application
2. Upload your Tally exports
3. Get instant AI insights!

**Time to Install:** 15-20 minutes (first time)
**Time to Run Daily:** 30 seconds

---

## 🌟 Pro Tips

1. **Create a shortcut** for easy daily access
2. **Backup data/** folder weekly
3. **Keep `.env` file** for custom settings
4. **Run on local network** to share with team
5. **Export reports** regularly for records

---

**Need help?** Check other documentation files:
- `README.md` - Overview
- `QUICK_START.md` - How to use
- `PACKAGES_GUIDE.md` - Features & pricing
- `FEATURES_IMPLEMENTED.md` - What's included

🚀 **Happy Trading with AI-Powered Insights!**
