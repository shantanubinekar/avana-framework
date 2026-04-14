# Quick Start Guide - AVAnA (Android Vulnerability Analysis Framework)

## 5-Minute Setup

### Step 1: Navigate to Project
```bash
cd /Users/shantanubinekar/Documents/vulnerability
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python3 run.py
```

### Step 5: Open in Browser
Navigate to `http://localhost:5000`

---

## Using the Application

### Dashboard Tab
- View statistics of all analyses
- See recent analyses
- Check top vulnerabilities

### Upload APK Tab
1. Click to select or drag-drop your APK file
2. Enter application name (optional)
3. Select analysis checkboxes:
   ✓ Permission Analysis
   ✓ Cryptography Analysis
   ✓ Injection Vulnerabilities
   ✓ Hardcoded Secrets
   ✓ WebView Issues
4. Click "Upload & Analyze"

### Analysis Tab
- View all detected vulnerabilities
- Filter by severity level
- Filter by vulnerability category
- Click on vulnerabilities for detailed information

### Reports Tab
- Download generated reports
- View analysis history

### Settings Tab
- Configure deep scan options
- Enable/disable decompiled code analysis
- Set auto-report generation

---

## Understanding Results

### Severity Levels
- 🔴 **Critical**: Fix immediately (Security breach risk)
- 🟠 **High**: Fix soon (Significant vulnerability)
- 🟡 **Medium**: Should address (Notable issue)
- 🔵 **Low**: Minor issue (Best practice)

### Vulnerability Categories

#### Permissions (HIGH RISK)
**What it is**: App requesting dangerous user data access
**Examples**: Camera, Location, Contacts, SMS
**Action**: Review if permission is truly needed; request user consent

#### Cryptography (MEDIUM-HIGH RISK)
**What it is**: Weak encryption or hashing methods
**Examples**: MD5, SHA-1, ECB mode
**Action**: Update to SHA-256, AES-GCM, or modern algorithms

#### Injection (HIGH RISK)
**What it is**: Vulnerabilities to code injection attacks
**Examples**: SQL injection, Command injection
**Action**: Use parameterized queries; avoid string concatenation

#### Hardcoded Secrets (CRITICAL)
**What it is**: Sensitive data embedded in code
**Examples**: Passwords, API keys, Tokens
**Action**: Move to secure backend; use environment variables

#### WebView (MEDIUM RISK)
**What it is**: Web content security issues
**Examples**: JavaScript enabled, XSS vulnerabilities
**Action**: Disable JavaScript if not needed; validate URLs

---

## Example APK Analysis

### Before Upload
- Ensure APK file is < 100MB
- APK should not be corrupted
- System needs 500MB free disk space for extraction

### During Analysis
- Framework extracts APK
- Scans AndroidManifest.xml
- Analyzes DEX files
- Checks resources and code
- Generates vulnerability list

### After Analysis
- Review each vulnerability
- Click for detailed recommendations
- Download report for documentation
- Plan remediation steps

---

## Common Use Cases

### 1. Pre-Release Check
```
Upload → Select all analysis options → Review results → Fix issues
```

### 2. Security Audit
```
Upload → Deep scan enabled → Generate report → Document findings
```

### 3. Third-Party App Review
```
Upload → Run analysis → Check critical issues → Rate security
```

### 4. Compliance Verification
```
Upload → Select compliance checks → Download report → Share with team
```

---

## Tips & Tricks

### For Faster Analysis
- Disable unnecessary checks if analyzing similar apps
- Close other programs to free RAM
- Use smaller APKs for testing

### For Better Results
- Enable "Deep Scan" for thorough analysis
- Include "Decompiled Code Analysis" for detailed checks
- Run analysis on release APKs, not debug builds

### For Reports
- Enable "Auto-generate PDF Reports"
- Download reports immediately after analysis
- Keep reports for compliance documentation

---

## Troubleshooting

### "Port 5000 already in use"
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
# Or use different port by editing run.py
```

### "Flask module not found"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### "APK won't upload"
- Check file is actually .apk format
- Verify file size < 100MB
- Try a different APK to rule out file corruption

### "Analysis results blank"
- Check browser console (F12) for errors
- Ensure JavaScript is enabled
- Try refreshing the page

---

## File Structure Created

```
vulnerability/
├── app/
│   ├── __init__.py                     # App module
│   ├── app.py                          # Flask main app
│   ├── static/
│   │   ├── css/style.css              # Desktop styling
│   │   └── js/main.js                 # Frontend logic
│   ├── templates/
│   │   └── index.html                 # UI layout
│   └── analysis/
│       ├── __init__.py
│       ├── vulnerability_analyzer.py   # Analysis engine
│       └── android_manifest_parser.py  # Manifest parser
├── uploads/                            # APK storage
├── venv/                              # Virtual environment
├── requirements.txt                   # Dependencies
├── run.py                             # Start script
├── README.md                          # Full documentation
└── QUICKSTART.md                      # This file
```

---

## API Quick Reference

### Upload and Start Analysis
```
POST /api/upload
Form Data: file, app_name, permission_check, crypto_check, ...
Response: { success: bool, analysis_id: string, vulnerabilities: [...] }
```

### Get Analysis Results
```
GET /api/analysis/{analysis_id}
Response: { vulnerabilities: [...], statistics: {...} }
```

### Get Dashboard Data
```
GET /api/dashboard
Response: { recent_analyses: [...], top_vulnerabilities: [...] }
```

---

## Next Steps

1. ✓ Setup complete
2. → Upload your first APK
3. → Review vulnerabilities
4. → Fix critical issues
5. → Re-analyze to verify fixes

---

## Need Help?

- **Framework Issues**: Check README.md
- **APK Problems**: Verify APK format and size
- **Browser Issues**: Clear cache, try different browser
- **Port Conflicts**: Change port in run.py

---

**Happy Analyzing! 🛡️**

*Android Vulnerability Analysis Framework v1.0*
