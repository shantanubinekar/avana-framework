"""
Configuration file for AVAnA Framework
Modify these settings to customize the application
"""

# Server Configuration
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

# File Upload Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB in bytes
ALLOWED_EXTENSIONS = {'apk', 'jar', 'xml'}

# Analysis Configuration
ANALYSIS_DEEP_SCAN_DEFAULT = True
ANALYSIS_DECOMPILE_CODE_DEFAULT = True
ANALYSIS_AUTO_PDF_DEFAULT = False

# Vulnerability Severity Settings
CRITICAL_VULN_THRESHOLD = 0  # Show all critical
HIGH_VULN_THRESHOLD = 0      # Show all high
MEDIUM_VULN_THRESHOLD = 15   # Show medium only if > 15 instances
LOW_VULN_THRESHOLD = 50      # Show low only if > 50 instances

# Security Settings
ENABLE_CORS = False  # Enable CORS for API
SECRET_KEY = 'your-secret-key-change-in-production'
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Feature Flags
ENABLE_PERMISSION_CHECK = True
ENABLE_CRYPTO_CHECK = True
ENABLE_INJECTION_CHECK = True
ENABLE_HARDCODED_CHECK = True
ENABLE_WEBVIEW_CHECK = True

# Dangerous Permissions List
DANGEROUS_PERMISSIONS = {
    'android.permission.CAMERA',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.ACCESS_COARSE_LOCATION',
    'android.permission.READ_CONTACTS',
    'android.permission.WRITE_CONTACTS',
    'android.permission.READ_CALENDAR',
    'android.permission.WRITE_CALENDAR',
    'android.permission.READ_CALL_LOG',
    'android.permission.WRITE_CALL_LOG',
    'android.permission.READ_SMS',
    'android.permission.SEND_SMS',
    'android.permission.RECEIVE_SMS',
    'android.permission.RECEIVE_MMS',
    'android.permission.READ_EXTERNAL_STORAGE',
    'android.permission.WRITE_EXTERNAL_STORAGE',
    'android.permission.GET_ACCOUNTS',
    'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS',
    'android.permission.BODY_SENSORS',
    'android.permission.MODIFY_AUDIO_SETTINGS',
    'android.permission.RECORD_AUDIO',
}

# Logging Configuration
ENABLE_LOGGING = True
LOG_FILE = 'logs/avana.log'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Performance Settings
CACHE_ENABLED = True
CACHE_TIMEOUT = 600  # seconds
MAX_WORKERS = 4  # For parallel processing

# UI Configuration
ITEMS_PER_PAGE = 20
AUTO_REFRESH_DASHBOARD = True
REFRESH_INTERVAL = 30  # seconds

# Export/Report Settings
EXPORT_FORMAT_OPTIONS = ['HTML', 'JSON', 'CSV']
DEFAULT_EXPORT_FORMAT = 'HTML'
AUTO_CLEANUP_OLD_REPORTS = False
REPORT_RETENTION_DAYS = 30

# Database Configuration (for future use)
DATABASE_URL = 'sqlite:///avana.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email Configuration (for notifications)
ENABLE_EMAIL_NOTIFICATIONS = False
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'

print("✓ Configuration loaded successfully")
