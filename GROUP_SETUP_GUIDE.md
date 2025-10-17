# 🚀 Montbridge Platform - Group Member Setup Guide

## ⚡ Quick Start (5 Minutes)

### Step 1: Get Python (If You Don't Have It)

**Check if you have Python:**
```bash
python3 --version
```

**If not installed:**
- Mac: `brew install python3` OR download from https://www.python.org
- Windows: Download from https://www.python.org/downloads/

---

### Step 2: Extract the Files

1. **Unzip** the file you received
2. **Open Terminal** (Mac) or **Command Prompt** (Windows)
3. **Navigate** to the folder:
   ```bash
   cd path/to/montbridge-platform
   # Or wherever you extracted the files
   ```

---

### Step 3: Setup (First Time Only)

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### Step 4: Run the Platform

**Start Backend:**
```bash
# Make sure venv is activated (you should see (venv) in your terminal)
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5001
* Running on http://127.0.0.1:5001
```

**Open Frontend:**
- Open your browser
- Navigate to the file: `index.html`
- Or double-click `index.html`

---

### Step 5: Use the Platform

1. **Click "Begin Analysis"**
2. **Enter company name** (e.g., "Acme Software Solutions Inc.")
3. **Upload files** from `sample_data/` folder:
   - Recommended: `acme_software_financials.csv`
   - Recommended: `acme_software_investment_memo.pdf.txt`
4. **Click "RUN COMPLETE ANALYSIS"**
5. **View results** in Dashboard, Valuation, and Risk tabs
6. **Download report**

---

## 📁 Sample Data Available

### Ready-to-Use Companies:

1. **Acme Software Solutions** (BEST FOR DEMO)
   - `acme_software_financials.csv`
   - `acme_software_investment_memo.pdf.txt`
   - High-growth SaaS company, $4.9M revenue, 30% growth

2. **BGSF, Inc.** (REAL SEC DATA)
   - `REAL_BGSF_Inc_financials.csv`
   - `REAL_BGSF_Inc_investment_memo.txt`
   - Real company from SEC filing, $125M revenue

3. **Greenleaf Manufacturing**
   - `greenleaf_manufacturing_financials.csv`
   - `greenleaf_manufacturing_memo.txt`
   - Sustainable packaging, $8.7M revenue

4. **Technology Solutions Inc.** (QUICK TEST)
   - `sample_financials.csv`
   - `sample_investment_memo.txt`
   - Simple test case, $1.2M revenue

---

## 🔧 Troubleshooting

### "Command not found: python3"
**Fix:** Use `python` instead of `python3`

### "pip: command not found"
**Fix:** Install pip: `python3 -m ensurepip --upgrade`

### "Module not found: flask"
**Fix:** Make sure venv is activated (you should see `(venv)` in terminal)

### Backend won't start
**Fix:** 
- Check port 5001 is not in use
- Try: `pkill -f "python app.py"` then restart

### Analysis fails
**Fix:** 
- Use `acme_software_financials.csv` (guaranteed to work)
- Check browser console (F12) for errors

---

## 💡 What Each Person Can Do

### Test the Platform:
- Upload different sample companies
- Compare valuations
- Review risk assessments
- Download reports

### Experiment:
- Try different companies
- Create your own financial data
- Modify assumptions
- Test edge cases

### For Presentation:
- Practice the demo flow
- Understand the calculations
- Know the key features
- Be ready for Q&A

---

## 📊 Platform Features

### What You Can Do:
- ✅ Upload financial statements (CSV/Excel)
- ✅ Upload investment memos (PDF/Word/TXT)
- ✅ Generate DCF valuations
- ✅ Compare with industry multiples
- ✅ Analyze precedent transactions
- ✅ Run sensitivity analysis
- ✅ Assess risks (High/Medium/Low)
- ✅ Download complete reports

### Technologies Used:
- **Backend**: Python, Flask, Pandas, NumPy
- **Frontend**: HTML, JavaScript, Chart.js
- **Analysis**: Financial modeling, NLP (optional)

---

## 🎯 Quick Commands Reference

### Start Platform:
```bash
cd montbridge-platform
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

### Stop Platform:
- Press `Ctrl+C` in the terminal

### Restart:
```bash
pkill -f "python app.py"  # Kill if stuck
python app.py  # Restart
```

### Check Backend Status:
```bash
curl http://localhost:5001/api/health
```

---

## 📞 Support

**If you have issues:**
1. Check TROUBLESHOOTING.md
2. Check README.md
3. Contact [Your Name/Email]
4. Check the console (F12 in browser)

---

## 🎓 For Demo Day

**Before the presentation:**
- [ ] Everyone has platform installed
- [ ] Everyone can run it successfully
- [ ] Test with sample data
- [ ] Practice the workflow
- [ ] Know how to explain features

**Recommended demo company:**
Use **Acme Software Solutions** - best growth story and metrics!

---

## ✅ Checklist for Group Members

- [ ] Python 3.8+ installed
- [ ] Files extracted
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend starts successfully (`python app.py`)
- [ ] Frontend opens in browser (`index.html`)
- [ ] Can upload files
- [ ] Analysis runs successfully
- [ ] Can download report
- [ ] Ready for demo!

---

**Questions? Check README.md or contact the team!**

