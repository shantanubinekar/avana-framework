# Advanced Features & Customization Guide

## Extending Analysis Capabilities

### Adding New Vulnerability Checks

To add a new vulnerability check, follow these steps:

#### 1. Add Function to `vulnerability_analyzer.py`

```python
def check_custom_vulnerability(self):
    """Check for custom vulnerabilities"""
    vulns = []
    
    # Your analysis logic here
    pattern = r'your_pattern_here'
    dex_files = self._find_files(self.extract_dir, '*.dex')
    
    for dex_file in dex_files:
        try:
            with open(dex_file, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
                
                if re.search(pattern, content):
                    vulns.append({
                        'title': 'Your Vulnerability Title',
                        'category': 'custom',
                        'severity': 'high',
                        'description': 'Vulnerability description',
                        'impact': 'Impact statement',
                        'recommendation': 'How to fix it',
                        'code_snippet': 'Pattern found'
                    })
        except Exception as e:
            pass
    
    return vulns
```

#### 2. Add to Flask API in `app.py`

```python
if custom_check:
    vulnerabilities.extend(analyzer.check_custom_vulnerability())
```

#### 3. Update HTML Form in `index.html`

```html
<label class="checkbox">
    <input type="checkbox" name="custom-check" checked>
    <span>Custom Vulnerability Check</span>
</label>
```

#### 4. Update Frontend in `main.js`

```javascript
formData.append('custom_check', 
    document.querySelector('input[name="custom-check"]').checked);
```

---

## Database Integration

### Setting Up SQLAlchemy for Data Persistence

#### 1. Install SQLAlchemy
```bash
pip install Flask-SQLAlchemy
pip install Flask-Migrate
```

#### 2. Create Models (`app/models.py`)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Analysis(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    app_name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, nullable=False)
    vuln_count = db.Column(db.Integer, default=0)
    file_path = db.Column(db.String(500))
    
    vulnerabilities = db.relationship('Vulnerability', backref='analysis', lazy=True)

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.String(50), db.ForeignKey('analysis.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))
    severity = db.Column(db.String(20))
    description = db.Column(db.Text)
    impact = db.Column(db.Text)
    recommendation = db.Column(db.Text)
```

#### 3. Update `app.py`

```python
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Analysis, Vulnerability

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avana.db'
db.init_app(app)

# Save analysis
analysis_record = Analysis(
    id=analysis_id,
    app_name=request.form.get('app_name'),
    filename=filename,
    timestamp=datetime.now(),
    vuln_count=len(vulnerabilities),
    file_path=filepath
)
db.session.add(analysis_record)

for vuln in vulnerabilities:
    vuln_record = Vulnerability(
        analysis_id=analysis_id,
        title=vuln['title'],
        category=vuln['category'],
        severity=vuln['severity'],
        description=vuln['description'],
        impact=vuln['impact'],
        recommendation=vuln['recommendation']
    )
    db.session.add(vuln_record)

db.session.commit()
```

---

## PDF Report Generation

### Using ReportLab for PDF Export

#### 1. Install ReportLab
```bash
pip install reportlab
```

#### 2. Create PDF Generator (`app/analysis/pdf_generator.py`)

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

class PDFReportGenerator:
    def __init__(self, analysis):
        self.analysis = analysis
    
    def generate(self, filepath):
        """Generate PDF report"""
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("<b>Android Vulnerability Analysis Report</b>", styles['Heading1'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Application Info
        info = f"""
        <b>Application:</b> {self.analysis['app_name']}<br/>
        <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        <b>File:</b> {self.analysis['filename']}<br/>
        """
        elements.append(Paragraph(info, styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Vulnerabilities
        elements.append(Paragraph("<b>Vulnerabilities</b>", styles['Heading2']))
        
        for vuln in self.analysis['vulnerabilities']:
            vuln_text = f"""
            <b>{vuln['title']}</b><br/>
            Severity: {vuln['severity'].upper()}<br/>
            Category: {vuln['category']}<br/>
            {vuln['description']}<br/>
            """
            elements.append(Paragraph(vuln_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        doc.build(elements)
```

---

## Authentication & User Management

### Basic Authentication Setup

#### 1. Install Flask-Login
```bash
pip install Flask-Login Flask-WTF
```

#### 2. Add Authentication to `app.py`

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
```

---

## Docker Deployment

### Dockerize the Application

#### Create `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "run.py"]
```

#### Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  avana:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    environment:
      - FLASK_ENV=production
      - DEBUG=False
```

#### Run with Docker

```bash
docker-compose up -d
```

---

## API Integration

### Webhook Support for CI/CD

```python
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """GitHub/GitLab webhook for automatic APK analysis"""
    data = request.get_json()
    
    # Download APK from URL
    apk_url = data.get('apk_url')
    
    if apk_url:
        # Download and analyze
        response = requests.get(apk_url)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'webhook_apk.apk')
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Analyze
        analyzer = VulnerabilityAnalyzer(filepath)
        vulnerabilities = analyzer.check_permissions()
        vulnerabilities.extend(analyzer.check_cryptography())
        
        # Return results
        return jsonify({
            'success': True,
            'vulnerabilities': vulnerabilities,
            'critical_count': len([v for v in vulnerabilities if v['severity'] == 'critical'])
        })
    
    return jsonify({'success': False}), 400
```

---

## Performance Optimization

### Caching Results

```python
from functools import lru_cache
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/dashboard')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_dashboard():
    # Your dashboard logic
    pass
```

### Async Processing with Celery

```bash
pip install celery redis
```

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379')

@celery.task
def analyze_apk_async(filepath):
    analyzer = VulnerabilityAnalyzer(filepath)
    return analyzer.check_all()
```

---

## Logging & Monitoring

### Advanced Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/avana.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

---

## Custom Threat Intelligence

### Integration with External APIs

```python
import requests

def check_virustotal(apk_hash):
    """Check APK hash on VirusTotal"""
    api_key = 'your_virustotal_api_key'
    url = f'https://www.virustotal.com/api/v3/files/{apk_hash}'
    headers = {'x-apikey': api_key}
    
    response = requests.get(url, headers=headers)
    return response.json()
```

---

## Testing

### Unit Tests

```python
import unittest

class TestVulnerabilityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = VulnerabilityAnalyzer('test.apk')
    
    def test_permission_check(self):
        results = self.analyzer.check_permissions()
        self.assertIsInstance(results, list)
    
    def test_crypto_check(self):
        results = self.analyzer.check_cryptography()
        self.assertIsInstance(results, list)

if __name__ == '__main__':
    unittest.main()
```

---

## Environment Variables

### Create `.env` file

```
DEBUG=False
SECRET_KEY=your-super-secret-key
DATABASE_URL=postgresql://user:password@localhost/avana
UPLOAD_FOLDER=/var/uploads
MAX_FILE_SIZE=104857600
VIRUSTOTAL_API_KEY=your_api_key
REDIS_URL=redis://localhost:6379/0
```

---

## Performance Benchmarks

### Typical Analysis Times
- Small APK (< 10MB): 5-15 seconds
- Medium APK (10-50MB): 20-60 seconds
- Large APK (50-100MB): 60-180 seconds

### Memory Requirements
- Minimum: 512MB RAM
- Recommended: 2GB RAM
- For large APKs: 4GB+ RAM

---

## Security Best Practices

1. **Run in sandboxed environment**
2. **Sanitize file uploads** - Already implemented
3. **Use HTTPS in production** - Add SSL certificate
4. **Rate limiting** - Prevent abuse
5. **Input validation** - Validate all user inputs
6. **Secure storage** - Encrypt sensitive data
7. **Regular backups** - Backup analysis data

---

## Troubleshooting Advanced Issues

### Memory Issues with Large APKs
- Increase swap space
- Process APKs in batches
- Implement streaming analysis

### Database Locks
- Check active connections
- Clear old sessions
- Use connection pooling

### Performance Degradation
- Clear old analysis files
- Optimize database queries
- Enable caching

---

**For more advanced customization, refer to Flask and Python documentation.**
