# DataSage AI - Installation Guide

### Option 1: Download & Run Locally

#### Step 1: Download
**[⬇️ Download DataSage AI ZIP file](https://github.com/your-username/datasage-ai/archive/refs/heads/main.zip)**

#### Step 2: Extract
- Windows: Right-click ZIP → "Extract All"
- Mac: Double-click ZIP file
- Linux: `unzip datasage-ai-main.zip`

#### Step 3: Install Python Dependencies
Open terminal/command prompt in the extracted folder:

```bash
# Install all required packages
pip install streamlit pandas numpy matplotlib seaborn scipy google-genai speechrecognition pyttsx3 reportlab weasyprint openpyxl

# ✅ Step-by-Step: Add GEMINI_API_KEY as a Windows Environment Variable
🔹 1. Get the Gemini API Key
Go to https://makersuite.google.com/app/apikey
Click "Create API key" (if you haven’t already).
Copy the key (starts with AI...)
🔹 2. Set Environment Variable on Windows
Press Win + S and type "environment variables", then click:

"Edit the system environment variables"

In the System Properties window, click the "Environment Variables…" button.

Under User variables, click New…

Variable name: GEMINI_API_KEY

Variable value: paste your actual API key here

Click OK on all windows to apply and close.

🔹 3. Restart Terminal or VSCode
This ensures your Python script picks up the new environment variable.

# Alternative: Use the automated installer
python run.py
```

#### Step 4: Get API Key (Free)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

#### Step 5: Set API Key
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Mac/Linux
export GEMINI_API_KEY=your_api_key_here
```

#### Step 6: Run Application
```bash
# Method 1: Use run script (recommended)
python run.py

# Method 2: Direct command
streamlit run app.py --server.port 5000
```

#### Step 7: Open Browser
Go to: `http://localhost:5000`

---

## 🔧 Platform-Specific Instructions

### Windows 10/11
1. Download ZIP file from link above
2. Extract to `C:\DataSage-AI\` (or preferred location)
3. Open Command Prompt:
   - Press `Win + R`, type `cmd`, press Enter
   - Navigate: `cd C:\DataSage-AI\`
4. Install dependencies: `pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl`
5. Run: `python run.py`

### macOS
1. Download ZIP file from link above
2. Extract to Desktop or preferred location
3. Open Terminal:
   - Press `Cmd + Space`, type "Terminal", press Enter
   - Navigate: `cd ~/Desktop/datasage-ai-main/`
4. Install dependencies: `pip3 install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl`
5. Run: `python3 run.py`

### Ubuntu/Linux
1. Download and extract:
   ```bash
   wget https://github.com/your-username/datasage-ai/archive/refs/heads/main.zip
   unzip main.zip
   cd datasage-ai-main
   ```
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
   ```
3. Run: `python3 run.py`

---

## 🐳 Docker Installation

### Quick Docker Setup
```bash
# Download project
git clone https://github.com/your-username/datasage-ai.git
cd datasage-ai

# Build and run with Docker
docker build -t datasage-ai .
docker run -p 5000:5000 -e GEMINI_API_KEY=your_api_key_here datasage-ai
```

### Dockerfile (included in project)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
```

---

## 🌐 Cloud Platform Deployments

### Streamlit Cloud (Free)
1. Fork the GitHub repository
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Deploy your forked repository
5. Add `GEMINI_API_KEY` in Advanced settings

### Heroku
1. Fork the repository
2. Create new Heroku app
3. Connect to GitHub repository
4. Add `GEMINI_API_KEY` to Config Vars
5. Deploy

### Railway
1. Go to [Railway](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your forked repository
4. Add `GEMINI_API_KEY` environment variable
5. Deploy

---

## 🛠️ Troubleshooting

### Python Not Found
**Windows:**
- Download Python from [python.org](https://python.org)
- Check "Add Python to PATH" during installation

**Mac:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Install Python
brew install python
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Pip Not Found
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
python3 -m ensurepip --upgrade
```

### Module Installation Errors
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with user flag
pip install --user streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl

# Use Python -m pip
python -m pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
```

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8501

# Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

### Excel Files Not Working
```bash
# Install Excel support
pip install openpyxl xlrd

# On Ubuntu/Debian
sudo apt-get install python3-openpyxl
```

### Voice Features Not Working
```bash
# Install audio dependencies
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
pip install speechrecognition pyttsx3

# macOS
brew install portaudio
pip install speechrecognition pyttsx3

# Windows (usually works by default)
pip install speechrecognition pyttsx3
```

### API Key Issues
1. Verify key is correct from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check environment variable is set: `echo $GEMINI_API_KEY`
3. Restart terminal after setting environment variable
4. On Replit: Add key to Secrets tab (not environment variables)

---

## 📋 System Requirements

### Minimum
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Python**: 3.8+
- **RAM**: 4GB
- **Storage**: 500MB free space
- **Internet**: Required for AI features

### Recommended
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.11
- **RAM**: 8GB+
- **Storage**: 2GB free space
- **CPU**: Multi-core processor

---

## 🆘 Still Need Help?

### Quick Solutions
1. **Can't install?** → Try Replit option (no installation needed)
2. **Python errors?** → Use `python3` instead of `python`
3. **Module errors?** → Run `pip install --upgrade pip` first
4. **Port errors?** → Change port in command: `--server.port 8501`
5. **API errors?** → Double-check your Gemini API key

### Get Support
- **Documentation**: See SETUP.md for detailed instructions
- **Issues**: Create issue on GitHub
- **Email**: support@datasage-ai.com

---

**✅ Installation Complete?** 
Open your browser to `http://localhost:5000` and start analyzing your data with AI!

*DataSage AI - Professional data analysis made simple*