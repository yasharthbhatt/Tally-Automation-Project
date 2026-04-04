# 📋 Client Deployment Checklist

## Pre-Deployment (Your Side)

### 1. Code Preparation
- [ ] All features tested and working
- [ ] No debug code or test data in production files
- [ ] `.env.example` is up to date with all required variables
- [ ] `requirements.txt` is current and complete
- [ ] All documentation is updated
- [ ] Remove `.env` file with real credentials
- [ ] Clear `logs/` folder
- [ ] Clear `data/` folder of test data

### 2. Files to Include
- [ ] All source code files (`*.py`)
- [ ] Installation scripts (`install.bat`, `install.sh`)
- [ ] Run scripts (`run_dashboard.bat`, `run_dashboard.sh`)
- [ ] `requirements.txt`
- [ ] `.env.example` (NOT `.env` with real keys!)
- [ ] All documentation files (`*.md`)
- [ ] Empty `data/` folder
- [ ] Empty `logs/` folder
- [ ] `README.md`
- [ ] `CLIENT_INSTALL_GUIDE.md`

### 3. Files to EXCLUDE
- [ ] `.venv/` (virtual environment)
- [ ] `__pycache__/` directories
- [ ] `.pyc` files
- [ ] `.env` file with real API keys
- [ ] `.git/` folder (if any)
- [ ] `.idea/` or `.vscode/` folders
- [ ] Personal test data
- [ ] `logs/` with old logs

### 4. Package Preparation
- [ ] Create clean folder structure
- [ ] Zip the project folder
- [ ] Test installation on fresh machine
- [ ] Document folder: `StockSense_v1.0_YYYYMMDD.zip`

### 5. Documentation Check
- [ ] Installation guide is clear
- [ ] Troubleshooting section is complete
- [ ] API key setup instructions (if applicable)
- [ ] Contact information is included
- [ ] Version number is documented

---

## Client Deployment Day

### Before Visiting Client

**Bring with you:**
- [ ] Project ZIP file on USB drive
- [ ] Backup on cloud/email
- [ ] Printed installation guide
- [ ] Python installer (offline backup)
- [ ] Your laptop (for testing)
- [ ] Client credentials/API keys (if pre-arranged)

### On Client's Machine

#### Step 1: System Check (5 min)
- [ ] Check OS version (Windows/Mac/Linux)
- [ ] Check available disk space (min 1 GB)
- [ ] Check RAM (min 4 GB, 8 GB preferred)
- [ ] Check internet connection
- [ ] Check admin/sudo access

#### Step 2: Python Installation (5 min)
- [ ] Check if Python is installed: `python --version`
- [ ] Install Python 3.9+ if needed
- [ ] Verify installation: `python --version`
- [ ] Verify pip: `pip --version`

#### Step 3: Project Installation (10 min)
- [ ] Extract project to desired location
- [ ] Note the installation path
- [ ] Run installation script
  - Windows: `install.bat`
  - Mac/Linux: `./install.sh`
- [ ] Wait for all dependencies to install
- [ ] Check for any error messages

#### Step 4: Configuration (5 min)
- [ ] Review `.env` file
- [ ] Add client's API keys (if applicable)
- [ ] Set client-specific parameters
- [ ] Configure thresholds if needed

#### Step 5: First Run (5 min)
- [ ] Start the application
  - Windows: `run_dashboard.bat`
  - Mac/Linux: `./run_dashboard.sh`
- [ ] Verify dashboard opens in browser
- [ ] Check all pages load correctly
- [ ] Verify no error messages

#### Step 6: Data Testing (10 min)
- [ ] Use client's sample Tally export
- [ ] Upload files through dashboard
- [ ] Process and analyze data
- [ ] Verify results are reasonable
- [ ] Check all visualizations render
- [ ] Export a sample report

#### Step 7: Training (15 min)
- [ ] Show how to start application
- [ ] Show how to stop application
- [ ] Demonstrate file upload process
- [ ] Walk through main features
- [ ] Show how to export reports
- [ ] Explain backup process

#### Step 8: Shortcuts & Convenience (5 min)
- [ ] Create desktop shortcut
  - Windows: Shortcut to `run_dashboard.bat`
  - Mac: Alias to `run_dashboard.sh`
- [ ] Test shortcut works
- [ ] Add to startup (if requested)

#### Step 9: Documentation Handover (5 min)
- [ ] Leave printed guide
- [ ] Show digital documentation location
- [ ] Explain troubleshooting section
- [ ] Provide support contact info
- [ ] Save important paths/settings

#### Step 10: Final Checks (5 min)
- [ ] Application starts successfully
- [ ] Client can operate independently
- [ ] Backup strategy explained
- [ ] Support process explained
- [ ] Payment/subscription activated (if applicable)

---

## Post-Deployment

### Immediate (Same Day)
- [ ] Send confirmation email to client
- [ ] Share digital copy of documentation
- [ ] Share any additional resources
- [ ] Note any special configurations made
- [ ] Schedule follow-up call (1 week)

### Follow-up (1 Week)
- [ ] Check if client is using system
- [ ] Address any issues
- [ ] Answer any questions
- [ ] Verify data processing is working
- [ ] Get initial feedback

### Follow-up (1 Month)
- [ ] Check system performance
- [ ] Review any feature requests
- [ ] Check if backup is being done
- [ ] Discuss any improvements
- [ ] Plan any updates

---

## Common Installation Issues & Solutions

### Issue: Python not found
**Solution:**
```bash
# Windows: Reinstall Python with "Add to PATH" checked
# Mac: brew install python@3.9
# Linux: sudo apt install python3.9 python3-pip
```

### Issue: pip install fails
**Solution:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Issue: Permission denied (Mac/Linux)
**Solution:**
```bash
chmod +x install.sh
chmod +x run_dashboard.sh
```

### Issue: Port 8501 in use
**Solution:**
```bash
streamlit run app_tally.py --server.port 8502
```

### Issue: Firewall blocking
**Solution:**
- Windows: Add exception in Windows Firewall
- Mac: System Preferences → Security → Firewall Options
- Linux: sudo ufw allow 8501

### Issue: Module not found
**Solution:**
```bash
# Activate virtual environment first!
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## Emergency Contacts

**Developer:**
- Name: [Your Name]
- Phone: [Your Phone]
- Email: [Your Email]

**Support Hours:**
- [Your Support Hours]

**Remote Access:**
- [TeamViewer/AnyDesk details if applicable]

---

## Version History

| Version | Date | Changes | Deployed To |
|---------|------|---------|-------------|
| 1.0 | YYYY-MM-DD | Initial release | - |
| | | | |

---

## Client Information Template

**Client Name:** _______________  
**Contact Person:** _______________  
**Email:** _______________  
**Phone:** _______________  
**Installation Date:** _______________  
**Installation Path:** _______________  
**OS:** _______________  
**Python Version:** _______________  
**Special Configurations:** _______________  
**API Keys Used:** _______________  
**Subscription Plan:** _______________  
**Next Follow-up:** _______________  

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Time Estimates

| Task | Estimated Time |
|------|---------------|
| System check | 5 minutes |
| Python installation | 5 minutes |
| Project installation | 10 minutes |
| Configuration | 5 minutes |
| First run & testing | 15 minutes |
| Training | 15 minutes |
| Setup convenience features | 5 minutes |
| Documentation | 5 minutes |
| **Total** | **60-70 minutes** |

---

**Remember:** 
- ✅ Stay calm and professional
- ✅ Document everything
- ✅ Test thoroughly before leaving
- ✅ Ensure client can operate independently
- ✅ Leave clear contact information

**Good luck with the deployment! 🚀**
