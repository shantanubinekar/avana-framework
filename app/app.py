import os
import json
import zipfile
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

# Import analysis modules
from app.analysis.vulnerability_analyzer import VulnerabilityAnalyzer
from app.analysis.android_manifest_parser import ManifestParser

# Get the absolute path to the app directory
app_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(app_dir, 'templates')
static_dir = os.path.join(app_dir, 'static')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'apk', 'jar', 'xml'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for analyses (in production, use a database)
analyses = {}
analysis_counter = 0


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle APK upload and analysis"""
    global analysis_counter
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'message': 'Only APK files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get analysis options
        permission_check = request.form.get('permission_check', 'false').lower() == 'true'
        crypto_check = request.form.get('crypto_check', 'false').lower() == 'true'
        injection_check = request.form.get('injection_check', 'false').lower() == 'true'
        hardcoded_check = request.form.get('hardcoded_check', 'false').lower() == 'true'
        webview_check = request.form.get('webview_check', 'false').lower() == 'true'
        
        # Perform analysis
        analyzer = VulnerabilityAnalyzer(filepath)
        vulnerabilities = []
        
        if permission_check:
            vulnerabilities.extend(analyzer.check_permissions())
        
        if crypto_check:
            vulnerabilities.extend(analyzer.check_cryptography())
        
        if injection_check:
            vulnerabilities.extend(analyzer.check_sql_injection())
        
        if hardcoded_check:
            vulnerabilities.extend(analyzer.check_hardcoded_secrets())
        
        if webview_check:
            vulnerabilities.extend(analyzer.check_webview_issues())
        
        # Store analysis
        analysis_counter += 1
        analysis_id = f'analysis_{analysis_counter}'
        
        analyses[analysis_id] = {
            'id': analysis_id,
            'app_name': request.form.get('app_name', filename),
            'file_path': filepath,
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities': vulnerabilities,
            'vuln_count': len(vulnerabilities),
            'analysis_options': {
                'permission_check': permission_check,
                'crypto_check': crypto_check,
                'injection_check': injection_check,
                'hardcoded_check': hardcoded_check,
                'webview_check': webview_check
            }
        }
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'message': f'Analysis complete. Found {len(vulnerabilities)} vulnerabilities.',
            'analysis': analyses[analysis_id]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/analysis/<analysis_id>')
def get_analysis(analysis_id):
    """Get analysis results"""
    if analysis_id not in analyses:
        return jsonify({'success': False, 'message': 'Analysis not found'}), 404
    
    analysis = analyses[analysis_id]
    return jsonify({
        'success': True,
        'analysis': analysis,
        'vulnerabilities': analysis['vulnerabilities']
    })


@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard data"""
    recent_analyses = []
    top_vulnerabilities = []
    
    # Get recent analyses (last 5)
    for analysis_id in sorted(analyses.keys(), reverse=True)[:5]:
        analysis = analyses[analysis_id]
        recent_analyses.append({
            'id': analysis_id,
            'app_name': analysis['app_name'],
            'timestamp': analysis['timestamp'],
            'vuln_count': analysis['vuln_count']
        })
    
    # Get top vulnerabilities
    all_vulns = {}
    for analysis in analyses.values():
        for vuln in analysis['vulnerabilities']:
            key = vuln['title']
            if key not in all_vulns:
                all_vulns[key] = {
                    'title': vuln['title'],
                    'severity': vuln['severity'],
                    'count': 0
                }
            all_vulns[key]['count'] += 1
    
    top_vulnerabilities = sorted(all_vulns.values(), key=lambda x: x['count'], reverse=True)
    
    return jsonify({
        'success': True,
        'recent_analyses': recent_analyses,
        'top_vulnerabilities': top_vulnerabilities,
        'total_analyses': len(analyses),
        'total_vulnerabilities': sum(a['vuln_count'] for a in analyses.values())
    })


@app.route('/api/reports/<analysis_id>/download')
def download_report(analysis_id):
    """Generate and download report"""
    if analysis_id not in analyses:
        return jsonify({'success': False, 'message': 'Analysis not found'}), 404
    
    analysis = analyses[analysis_id]
    
    # Generate HTML report
    html_content = generate_html_report(analysis)
    
    # Return as file
    from flask import send_file
    import io
    
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f'report_{analysis_id}.html')
    with open(pdf_path, 'w') as f:
        f.write(html_content)
    
    return send_file(pdf_path, as_attachment=True, download_name=f'report_{analysis_id}.html')


def generate_html_report(analysis):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Android Vulnerability Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .critical {{ color: #c0392b; }}
            .high {{ color: #e74c3c; }}
            .medium {{ color: #f39c12; }}
            .low {{ color: #3498db; }}
            .vuln-item {{ 
                border-left: 4px solid #ccc; 
                padding: 15px; 
                margin: 10px 0; 
                background: #f9f9f9;
            }}
            .vuln-item.critical {{ border-left-color: #c0392b; }}
            .vuln-item.high {{ border-left-color: #e74c3c; }}
            .vuln-item.medium {{ border-left-color: #f39c12; }}
            .vuln-item.low {{ border-left-color: #3498db; }}
            .badge {{ 
                display: inline-block; 
                padding: 5px 10px; 
                border-radius: 3px; 
                font-weight: bold; 
                font-size: 12px;
            }}
            .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
            .stat {{ padding: 15px; background: #f5f5f5; border-radius: 5px; }}
            .timestamp {{ color: #7f8c8d; font-size: 12px; }}
        </style>
    </head>
    <body>
        <h1>Android Vulnerability Analysis Report</h1>
        <p><strong>Application:</strong> {analysis['app_name']}</p>
        <p><strong>Date:</strong> {analysis['timestamp']}</p>
        <p><strong>File:</strong> {analysis['filename']}</p>
        
        <h2>Summary</h2>
        <div class="stats">
            <div class="stat">
                <strong>Total Vulnerabilities:</strong> {analysis['vuln_count']}
            </div>
            <div class="stat">
                <strong>Analysis Type:</strong> Static Analysis
            </div>
        </div>
        
        <h2>Vulnerabilities</h2>
    """
    
    if analysis['vulnerabilities']:
        for vuln in analysis['vulnerabilities']:
            severity_class = vuln['severity'].lower()
            html += f"""
            <div class="vuln-item {severity_class}">
                <h3>{vuln['title']}</h3>
                <p>
                    <span class="badge {severity_class}">{vuln['severity'].upper()}</span>
                    <span style="margin-left: 10px;">Category: {vuln['category']}</span>
                </p>
                <p><strong>Description:</strong> {vuln['description']}</p>
                <p><strong>Impact:</strong> {vuln['impact']}</p>
                <p><strong>Recommendation:</strong> {vuln['recommendation']}</p>
            </div>
            """
    else:
        html += "<p>No vulnerabilities detected.</p>"
    
    html += """
    </body>
    </html>
    """
    
    return html


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'success': False, 'message': 'File too large. Maximum size is 100MB'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
