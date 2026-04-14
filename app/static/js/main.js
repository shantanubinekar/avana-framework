// Navigation and Section Management
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const section = link.dataset.section;
        switchSection(section);
        updatePageTitle(section);
        link.classList.add('active');
        document.querySelectorAll('.nav-link').forEach(l => {
            if (l !== link) l.classList.remove('active');
        });
    });
});

function switchSection(section) {
    document.querySelectorAll('.section').forEach(s => {
        s.classList.remove('active');
    });
    document.getElementById(`${section}-section`).classList.add('active');
}

function updatePageTitle(section) {
    const titles = {
        'dashboard': 'Dashboard',
        'upload': 'Upload APK',
        'analysis': 'Analysis Results',
        'reports': 'Reports',
        'settings': 'Settings'
    };
    document.getElementById('page-title').textContent = titles[section] || 'Dashboard';
}

// File Upload Handler
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const uploadForm = document.getElementById('upload-form');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#3498db';
    uploadArea.style.backgroundColor = 'rgba(52, 152, 219, 0.05)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#bdc3c7';
    uploadArea.style.backgroundColor = '#f8f9fa';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#bdc3c7';
    uploadArea.style.backgroundColor = '#f8f9fa';
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect() {
    const file = fileInput.files[0];
    if (file && file.name.endsWith('.apk')) {
        document.getElementById('file-info').style.display = 'block';
        document.getElementById('file-name').textContent = file.name;
        document.getElementById('file-size').textContent = formatFileSize(file.size);
    } else if (file) {
        alert('Please select a valid APK file');
        fileInput.value = '';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Form Submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select an APK file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('app_name', document.getElementById('app-name').value || file.name);
    formData.append('permission_check', document.querySelector('input[name="permission-check"]').checked);
    formData.append('crypto_check', document.querySelector('input[name="crypto-check"]').checked);
    formData.append('injection_check', document.querySelector('input[name="injection-check"]').checked);
    formData.append('hardcoded_check', document.querySelector('input[name="hardcoded-check"]').checked);
    formData.append('webview_check', document.querySelector('input[name="webview-check"]').checked);

    showProgressModal();
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        hideProgressModal();

        if (result.success) {
            alert('Analysis complete! Check the Analysis tab for results.');
            switchSection('analysis');
            updatePageTitle('analysis');
            loadAnalysisResults(result.analysis_id);
            updateDashboard();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Upload error:', error);
        hideProgressModal();
        alert('Error uploading file: ' + error.message);
    }
});

// Modal Management
const modal = document.getElementById('vuln-modal');
const closeBtn = document.querySelector('.close');

closeBtn.addEventListener('click', () => {
    modal.classList.remove('show');
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.classList.remove('show');
    }
});

function showVulnerabilityDetail(vuln) {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h2>${vuln.title}</h2>
        <p><strong>Category:</strong> ${vuln.category}</p>
        <p><strong>Severity:</strong> <span class="severity-badge ${vuln.severity}">${vuln.severity.toUpperCase()}</span></p>
        <p><strong>Description:</strong></p>
        <p>${vuln.description}</p>
        <p><strong>Impact:</strong></p>
        <p>${vuln.impact}</p>
        <p><strong>Recommendation:</strong></p>
        <p>${vuln.recommendation}</p>
        ${vuln.code_snippet ? `<p><strong>Code Location:</strong></p><pre><code>${escapeHtml(vuln.code_snippet)}</code></pre>` : ''}
    `;
    modal.classList.add('show');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Progress Modal
const progressModal = document.getElementById('progress-modal');

function showProgressModal() {
    progressModal.style.display = 'flex';
    document.getElementById('progress-fill').style.width = '0%';
    document.getElementById('progress-text').textContent = 'Starting analysis...';
}

function hideProgressModal() {
    progressModal.style.display = 'none';
}

function updateProgress(percentage, message) {
    document.getElementById('progress-fill').style.width = percentage + '%';
    document.getElementById('progress-text').textContent = message;
}

// Load Analysis Results
async function loadAnalysisResults(analysisId) {
    try {
        const response = await fetch(`/api/analysis/${analysisId}`);
        const data = await response.json();

        const resultsContainer = document.getElementById('analysis-results');
        
        if (data.vulnerabilities && data.vulnerabilities.length > 0) {
            resultsContainer.innerHTML = data.vulnerabilities.map(vuln => `
                <div class="vulnerability-item ${vuln.severity}">
                    <div class="vuln-header">
                        <div>
                            <div class="vuln-title">${vuln.title}</div>
                            <div style="font-size: 12px; color: #7f8c8d; margin-top: 5px;">
                                <span class="vuln-category">${vuln.category}</span>
                            </div>
                        </div>
                    </div>
                    <span class="severity-badge ${vuln.severity}">${vuln.severity.toUpperCase()}</span>
                </div>
            `).join('');

            // Add click listeners
            document.querySelectorAll('.vulnerability-item').forEach((item, index) => {
                item.addEventListener('click', () => {
                    showVulnerabilityDetail(data.vulnerabilities[index]);
                });
            });
        } else {
            resultsContainer.innerHTML = '<p class="placeholder">No vulnerabilities detected.</p>';
        }

        // Update dashboard
        updateDashboardStats(data.vulnerabilities);
    } catch (error) {
        console.error('Error loading analysis results:', error);
    }
}

// Update Dashboard Stats
function updateDashboardStats(vulnerabilities) {
    const stats = {
        critical: 0,
        high: 0,
        medium: 0,
        low: 0
    };

    vulnerabilities.forEach(vuln => {
        stats[vuln.severity]++;
    });

    document.getElementById('critical-count').textContent = stats.critical;
    document.getElementById('high-count').textContent = stats.high;
    document.getElementById('medium-count').textContent = stats.medium;
    document.getElementById('low-count').textContent = stats.low;
}

// Update Dashboard
async function updateDashboard() {
    try {
        const response = await fetch('/api/dashboard');
        const data = await response.json();

        // Update recent analyses
        const recentAnalyses = document.getElementById('recent-analyses');
        if (data.recent_analyses && data.recent_analyses.length > 0) {
            recentAnalyses.innerHTML = data.recent_analyses.map(analysis => `
                <div class="analysis-item">
                    <div>
                        <div class="analysis-name">${analysis.app_name}</div>
                        <div class="analysis-date">${new Date(analysis.timestamp).toLocaleDateString()}</div>
                    </div>
                    <span class="analysis-badge">${analysis.vuln_count} Vulns</span>
                </div>
            `).join('');
        }

        // Update top vulnerabilities
        const topVulns = document.getElementById('top-vulns');
        if (data.top_vulnerabilities && data.top_vulnerabilities.length > 0) {
            topVulns.innerHTML = data.top_vulnerabilities.slice(0, 5).map(vuln => `
                <div style="padding: 10px; border-bottom: 1px solid #ecf0f1;">
                    <div style="font-weight: 500; margin-bottom: 5px;">${vuln.title}</div>
                    <span class="severity-badge ${vuln.severity}">${vuln.severity.toUpperCase()}</span>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// Filter Results
document.getElementById('severity-filter').addEventListener('change', filterResults);
document.getElementById('category-filter').addEventListener('change', filterResults);

function filterResults() {
    const severityFilter = document.getElementById('severity-filter').value;
    const categoryFilter = document.getElementById('category-filter').value;

    document.querySelectorAll('.vulnerability-item').forEach(item => {
        const severity = Array.from(item.classList).find(c => ['critical', 'high', 'medium', 'low'].includes(c));
        const category = item.querySelector('.vuln-category').textContent.toLowerCase();

        let show = true;
        if (severityFilter && severity !== severityFilter) show = false;
        if (categoryFilter && category !== categoryFilter) show = false;

        item.style.display = show ? 'flex' : 'none';
    });
}

// Settings
function saveSettings() {
    const deepScan = document.getElementById('deep-scan').checked;
    const decompileCode = document.getElementById('decompile-code').checked;
    const autoPdf = document.getElementById('auto-pdf').checked;

    const settings = { deepScan, decompileCode, autoPdf };
    localStorage.setItem('analysisSettings', JSON.stringify(settings));
    alert('Settings saved successfully!');
}

// Load settings on page load
function loadSettings() {
    const settings = localStorage.getItem('analysisSettings');
    if (settings) {
        const parsed = JSON.parse(settings);
        document.getElementById('deep-scan').checked = parsed.deepScan;
        document.getElementById('decompile-code').checked = parsed.decompileCode;
        document.getElementById('auto-pdf').checked = parsed.autoPdf;
    }
}

// Sidebar Toggle (Mobile)
const toggleBtn = document.querySelector('.toggle-sidebar');
const sidebar = document.querySelector('.sidebar');

toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking on a nav link (mobile)
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    updateDashboard();
});
