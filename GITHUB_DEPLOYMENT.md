# GitHub Deployment Guide

## 🚀 Quick Start from GitHub

### Method 1: Clone and Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/quote-management-system.git
cd quote-management-system

# 2. Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file from example
cp .env.example .env

# 5. Edit .env and add your API key
# Windows: notepad .env
# Linux/Mac: nano .env
# Add: ANTHROPIC_API_KEY=your_actual_api_key_here

# 6. Run the application
streamlit run app.py
```

### Method 2: Deploy to Streamlit Cloud (FREE!)

**Streamlit Cloud** offers free hosting for Streamlit apps!

#### Step-by-step:

1. **Push to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Sign in with GitHub

3. **Deploy New App**
   - Click "New app"
   - Select your repository
   - Choose branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

4. **Add Secrets** (IMPORTANT!)
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets" section
   - Add your secrets in TOML format:
   ```toml
   ANTHROPIC_API_KEY = "your_actual_api_key_here"
   ```

5. **Access Your App**
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Method 3: Deploy to Other Platforms

#### Heroku
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY=your_key_here
git push heroku main
```

#### Docker
```bash
# Build image
docker build -t quote-management-system .

# Run container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key_here \
  quote-management-system
```

## 🔒 Security Best Practices

### CRITICAL: Protect Your API Keys!

**❌ NEVER commit these files:**
- `.env` (contains actual API keys)
- `data/` directory (contains user data)
- Any file with passwords or secrets

**✅ Always commit these files:**
- `.env.example` (template without real keys)
- `.gitignore` (protects sensitive files)
- All source code files

### Before First Commit:

```bash
# 1. Check what will be committed
git status

# 2. Make sure .env is NOT listed
# If it is, add it to .gitignore immediately!

# 3. Double-check .gitignore exists
cat .gitignore

# 4. Verify sensitive files are ignored
git status --ignored
```

### If You Accidentally Committed Secrets:

**🚨 URGENT - Follow these steps:**

```bash
# 1. Immediately regenerate your API key at Anthropic console

# 2. Remove the file from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (WARNING: Rewrites history!)
git push origin --force --all

# 4. Add .env to .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
git push
```

## 📝 Code Changes for GitHub Deployment

### 1. Update API Key Loading (ALREADY DONE)

The code already uses environment variables:
```python
st.session_state.api_key = os.getenv('ANTHROPIC_API_KEY', '')
```

### 2. For Streamlit Cloud: Use Secrets

If deploying to Streamlit Cloud, update the code:

```python
# In app.py, add at the top:
import streamlit as st
import os

# Try to load from Streamlit secrets first, then environment variables
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
except:
    api_key = os.getenv('ANTHROPIC_API_KEY', '')

if 'api_key' not in st.session_state:
    st.session_state.api_key = api_key
```

### 3. Database Path Configuration

The current code already handles this well:
```python
db_path = os.getenv('DATABASE_PATH', 'data/quotes.db')
```

For Streamlit Cloud, you might want to ensure the data directory exists:
```python
# In src/database.py __init__ method
os.makedirs(os.path.dirname(db_path), exist_ok=True)
```

## 🌐 Repository Structure for GitHub

```
quote-management-system/
├── .github/
│   ├── workflows/          # GitHub Actions (optional)
│   └── ISSUE_TEMPLATE/     # Issue templates (optional)
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── claude_analyzer.py
│   └── database.py
├── docs/                   # Additional documentation (optional)
├── tests/                  # Unit tests (optional)
├── .gitignore             # CRITICAL - Protects secrets
├── .env.example           # Template for environment variables
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md              # Main documentation
├── LICENSE                # License file
├── run.sh                 # Linux/Mac startup script
└── run.bat                # Windows startup script
```

## 📦 Creating Your GitHub Repository

### Step-by-step:

1. **Create Repository on GitHub**
   - Go to https://github.com/new
   - Name: `quote-management-system`
   - Description: "Streamlit app for managing equipment quotations with PDF processing and AI analysis"
   - Public or Private (your choice)
   - **DO NOT** initialize with README (you already have one)
   - Click "Create repository"

2. **Initialize Local Git Repository**
   ```bash
   cd quote-management-system
   git init
   git add .
   git commit -m "Initial commit: Equipment Quote Management System"
   ```

3. **Connect to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/quote-management-system.git
   git branch -M main
   git push -u origin main
   ```

4. **Verify Upload**
   - Check https://github.com/YOUR_USERNAME/quote-management-system
   - Ensure `.env` is **NOT** visible (should be ignored)
   - Ensure `.env.example` **IS** visible

## 🔧 Configuration for Different Environments

### Local Development
```bash
# .env file
ANTHROPIC_API_KEY=your_dev_key_here
DATABASE_PATH=data/quotes.db
```

### Streamlit Cloud
```toml
# In Streamlit Cloud Secrets
ANTHROPIC_API_KEY = "your_production_key_here"
```

### Heroku
```bash
heroku config:set ANTHROPIC_API_KEY=your_production_key_here
heroku config:set DATABASE_PATH=/app/data/quotes.db
```

## 🐛 Troubleshooting

### Issue: "Permission denied" on run.sh
```bash
chmod +x run.sh
./run.sh
```

### Issue: Database file not found
```bash
mkdir -p data
python -c "from src.database import QuoteDatabase; QuoteDatabase()"
```

### Issue: Module not found
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Streamlit Cloud deployment fails
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility (3.9+)
- Check logs in Streamlit Cloud dashboard

## 📊 Optional Enhancements

### Add GitHub Actions for CI/CD

Create `.github/workflows/test.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest tests/
```

### Add Unit Tests

Create `tests/test_basic.py`:
```python
def test_import_modules():
    from src.pdf_processor import PDFProcessor
    from src.claude_analyzer import ClaudeAnalyzer
    from src.database import QuoteDatabase
    assert True
```

## 🤝 Collaboration

### For Contributors:

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/quote-management-system.git

# 3. Create a branch
git checkout -b feature/your-feature-name

# 4. Make changes and commit
git add .
git commit -m "Add your feature"

# 5. Push to your fork
git push origin feature/your-feature-name

# 6. Create Pull Request on GitHub
```

## 📄 License

Add a LICENSE file (e.g., MIT License) to clarify usage rights.

## 🎉 Success Checklist

- [ ] Repository created on GitHub
- [ ] `.gitignore` in place
- [ ] `.env` NOT committed
- [ ] `.env.example` committed
- [ ] All source files committed
- [ ] README.md updated with clone instructions
- [ ] App tested locally after cloning
- [ ] Secrets configured (if deploying to cloud)
- [ ] App deployed successfully

## 📞 Getting Help

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions or share ideas
- Pull Requests: Contribute improvements

---

**You're all set for GitHub! 🚀**

Remember: **NEVER commit your `.env` file or API keys!**
