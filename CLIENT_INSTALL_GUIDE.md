# 🚀 StockSense - Client Installation Guide

**Quick & Simple Installation for Client Machines**

---

## ✅ Before You Start

**What You Need:**
- Windows 10/11, macOS, or Linux
- Internet connection (for initial setup only)
- 500 MB free disk space
- 15 minutes

---

## 🎯 Installation Steps (3 Steps)

### Step 1: Install Python (if not already installed)

**Check if Python is installed:**
```bash
python --version
```

**If you see Python 3.9 or higher, skip to Step 2!**

**If not installed:**

**Windows Users:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.9 or higher
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click "Install Now"

**Mac Users:**
```bash
brew install python@3.9
```

**Linux Users (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip
```

---

### Step 2: Run the Automated Installer

**Extract the project folder to your desired location**

**Windows:**
1. Right-click `install.bat`
2. Select "Run as Administrator"
3. Wait for installation to complete

**Mac/Linux:**
1. Open Terminal in project folder
2. Run: `chmod +x install.sh`
3. Run: `./install.sh`
4. Wait for installation to complete

**The installer will:**
- ✅ Create a virtual environment
- ✅ Install all required packages
- ✅ Set up configuration files
- ✅ Create necessary directories

---

### Step 3: Start the Application

**Windows:**
- Double-click `run_dashboard.bat`

**Mac/Linux:**
- Double-click `run_dashboard.sh`
- Or in Terminal: `./run_dashboard.sh`

**The dashboard will open automatically at:** `http://localhost:8501`

---

## 🎉 You're Done!

The StockSense dashboard should now be running in your browser.

---

## 📤 Using the Application

### First Time Setup:

1. **Prepare Your Tally Data:**
   - Export product-wise reports from Tally
   - Export customer ledger report
   - Save as Excel files

2. **Upload in Dashboard:**
   - Open the dashboard
   - Use the sidebar to upload files
   - Click "Process & Analyze"

3. **View Insights:**
   - Navigate through different sections
   - View AI-powered insights
   - Export reports as needed

---

## 🔄 Daily Usage

**To start the application each day:**

**Windows:** Double-click `run_dashboard.bat`

**Mac/Linux:** Run `./run_dashboard.sh`

**To stop the application:**
- Press `Ctrl + C` in the terminal window
- Or simply close the terminal

---

## 🔧 Quick Troubleshooting

### Issue: "Python not found"
**Solution:** 
- Reinstall Python
- Make sure "Add Python to PATH" is checked (Windows)

### Issue: "Port already in use"
**Solution:**
```bash
streamlit run app_tally.py --server.port 8502
```

### Issue: Module errors
**Solution:**
```bash
# Activate virtual environment first
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# Then reinstall
pip install -r requirements.txt --force-reinstall
```

### Issue: Dashboard won't open
**Solution:**
- Check if firewall is blocking
- Manually open: `http://localhost:8501`
- Try different browser

---

## 🔐 Optional: API Keys Setup (AI Plus Features)

If you have subscribed to AI Plus package:

1. Create account on [OpenAI](https://platform.openai.com/) or [Anthropic](https://console.anthropic.com/)
2. Get your API key
3. Open `.env` file in project folder
4. Add your key:
   ```
   OPENAI_API_KEY=your_key_here
   # or
   ANTHROPIC_API_KEY=your_key_here
   ```
5. Restart the application

---

## 💾 Backup Your Data

**Important folders to backup regularly:**
- `data/` - All your business data
- `.env` - Your configuration settings

**Simple backup command:**

**Windows:**
```cmd
xcopy data data_backup /E /I
```

**Mac/Linux:**
```bash
cp -r data/ data_backup/
```

---

## 🌐 Network Access (Optional)

To access from other computers on your network:

1. **On the server computer:**
   ```bash
   streamlit run app_tally.py --server.address 0.0.0.0
   ```

2. **Find your IP address:**
   - Windows: Run `ipconfig`
   - Mac/Linux: Run `ifconfig`
   - Look for IP like `192.168.1.100`

3. **On other computers:**
   - Open browser
   - Go to: `http://192.168.1.100:8501`

**Note:** Only use on trusted local networks

---

## 📞 Support Contacts

**For technical support:**
- Check `INSTALLATION.md` for detailed instructions
- Check `README.md` for feature details
- Review error messages in terminal

**For subscription/payment issues:**
- See `SUBSCRIPTION_SETUP.md`

---

## ✅ Post-Installation Checklist

- [ ] Python installed and working
- [ ] Installation script completed successfully
- [ ] Dashboard opens in browser
- [ ] Can upload sample files
- [ ] Analysis runs without errors
- [ ] Can view insights and reports
- [ ] Backup strategy in place

---

## 🎯 Quick Reference

| Action | Windows | Mac/Linux |
|--------|---------|-----------|
| Install | `install.bat` | `./install.sh` |
| Run | `run_dashboard.bat` | `./run_dashboard.sh` |
| Stop | `Ctrl + C` | `Ctrl + C` |
| Port | 8501 | 8501 |

---

## 🚀 Ready to Use!

**Estimated Setup Time:** 15 minutes  
**Daily Start Time:** 30 seconds

Your AI-powered inventory intelligence system is ready to transform your business insights!

---

*For detailed technical documentation, see `INSTALLATION.md`*
