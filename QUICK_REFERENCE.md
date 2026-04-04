# 📋 StockSense - Quick Reference Card

**Print this page for easy reference**

---

## 🚀 Daily Usage

### Start Application

**Windows:**
```
Double-click: run_dashboard.bat
```

**Mac/Linux:**
```
Run: ./run_dashboard.sh
```

**Dashboard opens at:** `http://localhost:8501`

### Stop Application
Press `Ctrl + C` in the terminal window

---

## 📤 Upload Data

1. **Export from Tally:**
   - Product-wise reports
   - Customer ledger report
   - Save as Excel files

2. **Upload in Dashboard:**
   - Click sidebar "Upload Files"
   - Select your Excel files
   - Click "Process & Analyze"

3. **View Results:**
   - Navigate through sections
   - View charts and insights
   - Export reports as needed

---

## 🔧 Common Issues

| Problem | Solution |
|---------|----------|
| Dashboard won't open | Open browser to `http://localhost:8501` |
| Port in use | Use: `streamlit run app_tally.py --server.port 8502` |
| Module not found | Activate venv, then: `pip install -r requirements.txt` |
| Python not found | Reinstall Python with "Add to PATH" checked |

---

## 📞 Support

**Technical Issues:**
- Check `CLIENT_INSTALL_GUIDE.md`
- Check `INSTALLATION.md` for detailed help
- Review error messages in terminal

**Contact:**
- Developer: [Your Name]
- Email: [Your Email]
- Phone: [Your Phone]

---

## 💾 Backup

**Important folders:**
- `data/` - Your business data
- `.env` - Your settings

**Backup command:**

**Windows:**
```cmd
xcopy data data_backup /E /I
```

**Mac/Linux:**
```bash
cp -r data/ data_backup/
```

**Frequency:** Weekly or before major updates

---

## ⚙️ File Locations

| Item | Location |
|------|----------|
| Installation | `[Your installation path]` |
| Data files | `data/` folder |
| Logs | `logs/` folder |
| Config | `.env` file |
| Documentation | `*.md` files |

---

## 🌐 Network Access (Optional)

**To share on local network:**

1. **Run with network access:**
   ```bash
   streamlit run app_tally.py --server.address 0.0.0.0
   ```

2. **Find your IP:**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig`

3. **Other computers access via:**
   ```
   http://[YOUR_IP]:8501
   Example: http://192.168.1.100:8501
   ```

---

## 🔑 API Keys (AI Plus Only)

**If using AI Plus features:**

1. Get API key from:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. Edit `.env` file:
   ```
   OPENAI_API_KEY=your_key_here
   ```

3. Restart application

---

## 📊 System Requirements

- **OS:** Windows 10+, macOS 10.14+, Linux
- **RAM:** 4 GB minimum (8 GB recommended)
- **Storage:** 500 MB free space
- **Python:** 3.9 or higher
- **Internet:** For installation only

---

## ✅ Quick Checklist

**Daily startup:**
- [ ] Run dashboard script
- [ ] Dashboard opens in browser
- [ ] Upload data files
- [ ] Review insights
- [ ] Export reports (optional)

**Weekly maintenance:**
- [ ] Backup `data/` folder
- [ ] Check for updates
- [ ] Review logs (optional)

---

## 🎯 Key Features

✅ Data upload and processing  
✅ AI-powered forecasting  
✅ Customer segmentation  
✅ Automated insights  
✅ Interactive charts  
✅ Export reports  
✅ Low stock alerts  
✅ Reorder recommendations  

---

## 📖 Documentation Files

- `CLIENT_INSTALL_GUIDE.md` - Installation help
- `QUICK_START.md` - How to use features
- `INSTALLATION.md` - Detailed setup
- `README.md` - Overview
- `FEATURES_IMPLEMENTED.md` - Full feature list

---

## 🔄 Version Info

**Current Version:** Check `VERSION.txt`

**Update Process:**
1. Backup your data
2. Extract new version
3. Run: `pip install -r requirements.txt --upgrade`
4. Restart application

---

## ⚡ Keyboard Shortcuts

**In Terminal:**
- `Ctrl + C` - Stop application
- `Ctrl + Z` - Suspend (not recommended)

**In Browser:**
- `F5` - Refresh dashboard
- `Ctrl + Shift + R` - Hard refresh

---

## 🌟 Tips

💡 **Create Desktop Shortcut** for one-click access  
💡 **Backup regularly** - Don't lose your data!  
💡 **Close other programs** if application is slow  
💡 **Use Chrome/Firefox** for best experience  
💡 **Keep Python updated** for security  

---

## 📅 Maintenance Schedule

**Daily:**
- Use the application
- Process new Tally exports

**Weekly:**
- Backup data folder
- Clear old logs (optional)

**Monthly:**
- Check for application updates
- Review insights trends
- Archive old reports

---

**🚀 Happy Trading with AI-Powered Insights!**

*Keep this card handy for quick reference*

---

*Last Updated: [Date]*  
*Version: 1.0*
