# How to Upload AVAnA to GitHub/Git

## Prerequisites

Before uploading, ensure you have:
- Git installed (`git --version`)
- A GitHub account (https://github.com)
- Git configured with your credentials

## Step 1: Configure Git (First Time Only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `avana-framework` (or your preferred name)
3. Description: `Android Vulnerability Analysis Framework - Static Analysis Tool`
4. Choose: **Public** (to share) or **Private** (for personal use)
5. Click "Create repository"
6. Copy the repository URL (e.g., https://github.com/YOUR_USERNAME/avana-framework.git)

## Step 3: Initialize Local Git Repository

```bash
# Navigate to project
cd /Users/shantanubinekar/Documents/vulnerability

# Initialize git
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: AVAnA framework v1.0 - Android vulnerability analysis tool"

# Add remote repository (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/avana-framework.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Verify Upload

Visit your GitHub repository URL to confirm all files are uploaded.

---

## 🔥 Quick Command (Copy & Paste)

```bash
cd /Users/shantanubinekar/Documents/vulnerability

# Set your info
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize and commit
git init
git add .
git commit -m "Initial commit: AVAnA framework v1.0 - Android vulnerability static analysis"

# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/avana-framework.git
git branch -M main
git push -u origin main
```

---

## 📝 Create .gitignore File

To avoid uploading unnecessary files, create a `.gitignore`:

```bash
echo "# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# APK uploads
uploads/*.apk
uploads/*.jar

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Cache
.cache/
.pytest_cache/

# Database
*.db
*.sqlite
" > .gitignore

git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## 🔄 Future Updates

After making changes:

```bash
# Add changes
git add .

# Commit with message
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

---

## 🆘 Troubleshooting

### Error: "Repository not found"
- Check GitHub username and repository name
- Verify URL is correct
- Ensure you have write permissions

### Error: "fatal: could not read Username"
```bash
git config --global credential.helper osxkeychain
```

### Error: "No changes added to commit"
```bash
git add .
git status  # Check what's being tracked
```

### View Git History
```bash
git log
git log --oneline
git status
```

---

## 📌 Useful Git Commands

```bash
# Check status
git status

# View history
git log --oneline

# Create a new branch
git branch feature-name
git checkout feature-name

# Delete local repository
rm -rf .git

# Clone your repository elsewhere
git clone https://github.com/YOUR_USERNAME/avana-framework.git
```

---

## 🎯 Complete Workflow

```bash
# 1. Initial setup (one time)
cd /Users/shantanubinekar/Documents/vulnerability
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/avana-framework.git
git branch -M main
git push -u origin main

# 2. Making changes
echo "# Updated README" > README.md
git add README.md
git commit -m "Update README"
git push origin main

# 3. Creating versions/releases
git tag v1.0.0
git push origin v1.0.0
```

---

## 📦 Push to Other Platforms

### GitLab
```bash
git remote add origin https://gitlab.com/YOUR_USERNAME/avana-framework.git
git push -u origin main
```

### Bitbucket
```bash
git remote add origin https://bitbucket.org/YOUR_USERNAME/avana-framework.git
git push -u origin main
```

---

**Done! Your AVAnA framework is now on GitHub!** 🎉
