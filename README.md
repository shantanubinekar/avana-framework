# Android Vulnerability Static Analysis Framework (AVAnA)

A comprehensive HTML-based framework for performing static analysis of vulnerabilities in Android applications. This tool helps developers identify and fix security issues in their APK files.

## Features

### 🔍 Security Analysis
- **Permission Analysis**: Detect dangerous permissions usage
- **Cryptography Analysis**: Identify weak cryptographic implementations
- **SQL Injection Detection**: Find potential SQL injection vulnerabilities
- **Hardcoded Secrets**: Locate hardcoded credentials and API keys
- **WebView Security**: Check for WebView security misconfigurations

### 📊 Dashboard & Reporting
- Real-time vulnerability statistics
- Severity-based vulnerability classification (Critical, High, Medium, Low)
- Detailed vulnerability reports with recommendations
- HTML report generation
- Historical analysis tracking

### 🎨 Modern UI
- Responsive design for desktop and mobile
- Dark-themed dashboard
- Interactive navigation
- Real-time progress tracking
- Detailed vulnerability modal views

## System Requirements

- Python 3.7+
- Flask 3.0.0
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 100MB disk space for APK analysis

## Installation

### 1. Clone/Setup the Project
```bash
git clone https://github.com/shantanubinekar/avana-framework.git
cd avana-framework
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application
```bash
python3 run.py
```

The application will start on `http://localhost:5000`

### Uploading an APK
1. Go to the "Upload APK" section
2. Drag and drop your APK file or click to browse
3. Select analysis options:
   - Permission Analysis
   - Cryptography Analysis
   - Injection Vulnerabilities
   - Hardcoded Secrets
   - WebView Issues
4. Click "Upload & Analyze"
5. View results in the "Analysis" tab

### Analyzing Results
- View vulnerability details by clicking on each item
- Filter by severity (Critical, High, Medium, Low)
- Filter by category (Permissions, Cryptography, Injection, Hardcoded, WebView)
- Download reports for detailed analysis

### Dashboard
The dashboard shows:
- Total vulnerability counts by severity
- Recent analyses
- Top detected vulnerabilities
- Quick statistics overview

## Project Structure

```
vulnerability/
├── app/
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── vulnerability_analyzer.py    # Main analysis engine
│   │   └── android_manifest_parser.py   # Manifest parsing
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css               # UI styling
│   │   └── js/
│   │       └── main.js                 # Frontend logic
│   ├── templates/
│   │   └── index.html                  # Main interface
│   └── app.py                          # Flask application
├── uploads/                            # APK storage
├── requirements.txt                    # Python dependencies
├── run.py                              # Entry point
└── README.md                           # This file
```

## API Endpoints

### Upload & Analysis
- `POST /api/upload` - Upload APK and start analysis
- `GET /api/analysis/<analysis_id>` - Get analysis results
- `GET /api/dashboard` - Get dashboard data
- `GET /api/reports/<analysis_id>/download` - Download report

## Vulnerability Categories

### 1. Permissions (High Risk)
- Camera access
- Location tracking
- Contact access
- SMS reading/sending
- Call log access

### 2. Cryptography (Medium-High Risk)
- Weak hash algorithms (MD5, SHA-1)
- Insecure random number generation
- ECB mode encryption
- Weak key sizes

### 3. Injection Attacks (High Risk)
- SQL injection vulnerabilities
- Command injection risks
- XML/XPath injection

### 4. Hardcoded Secrets (Critical)
- Hardcoded passwords
- API keys in code
- Private keys exposure
- Database credentials

### 5. WebView Issues (Medium Risk)
- JavaScript enabled without need
- URL scheme abuse
- Cross-site scripting (XSS)
- Unsafe file access

## Configuration

### Settings Available
- **Deep Scan**: Enable comprehensive analysis
- **Include Decompiled Code Analysis**: Analyze decompiled source
- **Auto-generate PDF Reports**: Automatically create reports

Modify settings in the Settings tab to customize analysis behavior.

## Vulnerability Severity Levels

- 🔴 **Critical**: Immediate action required
- 🟠 **High**: Significant security risk
- 🟡 **Medium**: Should be addressed
- 🔵 **Low**: Minor issue, can be noted

## Sample Analysis Output

Each vulnerability includes:
- **Title**: Vulnerability name
- **Severity**: Risk level
- **Category**: Type of vulnerability
- **Description**: What the vulnerability is
- **Impact**: Potential consequences
- **Recommendation**: How to fix it
- **Code Location**: Where it was found in the APK

## Limitations

- APK size limit: 100MB
- Requires APK format (not AAB/AAX)
- Decompilation analysis may not work on obfuscated code
- Dynamic analysis capabilities not included
- Requires internet connection for initial setup

## Best Practices

1. **Regular Scanning**: Scan APKs before each release
2. **Address Critical Issues**: Fix all critical vulnerabilities
3. **Update Dependencies**: Keep libraries current
4. **Code Review**: Use results to improve development practices
5. **Secure Coding**: Follow Android security guidelines

## Android Security Guidelines

- [Android Security Documentation](https://developer.android.com/security)
- [OWASP Mobile Top 10](https://owasp.org/www-project-mobile-top-10/)
- [Google Play Security Policy](https://support.google.com/googleplay/android-developer/answer/9859455)

## Troubleshooting

### APK Upload Fails
- Check file size (max 100MB)
- Verify APK is not corrupted
- Ensure proper APK format

### No Results Displayed
- Check browser console for errors
- Verify analysis options are selected
- Try with a different APK

### Server Won't Start
- Check if port 5000 is available
- Verify Python version (3.7+)
- Reinstall Flask: `pip install --upgrade Flask`

## Contributing

To extend the framework:
1. Add new vulnerability checks in `vulnerability_analyzer.py`
2. Update the UI in `index.html` for new features
3. Add API endpoints in `app.py`

## Performance Tips

- Smaller APKs analyze faster
- Disable unnecessary analysis options for speed
- Close other applications to free RAM
- Use an SSD for faster APK extraction

## Future Enhancements

- [ ] Support for AAB format
- [ ] Dynamic analysis capabilities
- [ ] Machine learning-based detection
- [ ] Cloud-based analysis
- [ ] Team collaboration features
- [ ] CI/CD integration
- [ ] PDF report generation
- [ ] Database for historical tracking
- [ ] API key management

## License

This framework is provided for educational and authorized security testing purposes only.

## Disclaimer

This tool should only be used to analyze applications you own or have permission to analyze. Unauthorized analysis of applications may violate laws and terms of service.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the vulnerabilities documentation
3. Ensure all dependencies are properly installed

## Version

**AVAnA v1.0.0** - Initial Release
- Basic vulnerability detection
- Web-based interface
- Report generation
- Dashboard analytics

---

**Android Vulnerability Analysis Framework (AVAnA)**
*Making Android Security Analysis Accessible*
