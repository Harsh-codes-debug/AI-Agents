# DataSage AI - Download Links & Distribution

## 📥 Quick Download Options

### Option 1: Direct Download (Recommended)
Download the complete DataSage AI application as a ZIP file:

**[⬇️ Download DataSage AI v2.0](https://github.com/your-username/datasage-ai/archive/refs/heads/main.zip)**

### Option 2: Clone Repository
```bash
git clone https://github.com/your-username/datasage-ai.git
cd datasage-ai
```

### Option 3: Replit Template
**[🚀 Use Replit Template](https://replit.com/@your-username/DataSage-AI)**
- One-click setup
- No installation required
- Automatic dependency management

## 📋 What's Included

```
datasage-ai/
├── app.py                      # Main application
├── demo_data.csv              # Clean sample dataset
├── demo_dirty_data.csv        # Sample dataset with quality issues
├── SETUP.md                   # Complete setup guide
├── README.md                  # Project overview
├── dependencies.txt           # Installation guide
├── run.py                     # Easy startup script
├── modules/
│   ├── eda.py                 # Data analysis
│   ├── chart_gen.py           # Visualizations
│   ├── gemini_live.py         # AI assistant
│   ├── data_cleaning.py       # Data cleaning tools
│   ├── voice_handler.py       # Voice features
│   └── export.py              # Data export
└── assets/
    └── dark_mode.css          # Custom styling
```

## 🚀 Quick Start After Download

### 1. Install Dependencies
```bash
pip install streamlit pandas numpy matplotlib seaborn scipy google-genai speechrecognition pyttsx3 reportlab weasyprint openpyxl
```

### 2. Set API Key
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Run Application
```bash
# Option A: Using run script (recommended)
python run.py

# Option B: Direct streamlit
streamlit run app.py --server.port 5000
```

### 4. Open Browser
Navigate to: `http://localhost:5000`

## 🔧 Platform-Specific Downloads

### Windows Users
1. Download ZIP file
2. Extract to desired folder
3. Open Command Prompt in extracted folder
4. Run: `pip install -r requirements.txt` (if available) or use dependencies from SETUP.md
5. Run: `python run.py`

### Mac/Linux Users
1. Download ZIP or clone repository
2. Open Terminal in project folder
3. Run: `pip3 install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl`
4. Run: `python3 run.py`

### Docker Users
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
EXPOSE 5000
CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
```

## 📦 Distribution Packages

### Python Package (PyPI) - Coming Soon
```bash
pip install datasage-ai
datasage-ai --start
```

### Standalone Executable - Coming Soon
- Windows: `DataSage-AI-Windows.exe`
- macOS: `DataSage-AI-macOS.dmg`
- Linux: `DataSage-AI-Linux.AppImage`

## 🌐 Online Versions

### Streamlit Cloud (Free)
**[🌐 Try Online](https://your-app.streamlit.app)**
- No installation required
- Limited to free tier resources
- Perfect for testing and light usage

### Replit (Free/Paid)
**[🔗 Open in Replit](https://replit.com/@your-username/DataSage-AI)**
- Instant setup
- Collaborative editing
- Built-in deployment

### Google Colab (Free)
```python
!git clone https://github.com/your-username/datasage-ai.git
%cd datasage-ai
!pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
!streamlit run app.py --server.port 8501 &
```

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for AI features

### Recommended Specifications
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.11
- **RAM**: 8GB or more
- **Storage**: 2GB free space
- **CPU**: Multi-core processor
- **Internet**: Stable broadband connection

## 🔑 API Key Setup

### Get Free Gemini API Key
1. Visit: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key
5. Add to environment variables or Replit Secrets

### Environment Variable Setup
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Mac/Linux
export GEMINI_API_KEY=your_api_key_here

# Using .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## 🆘 Installation Help

### Common Issues

**"ModuleNotFoundError"**
```bash
pip install --upgrade pip
pip install streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
```

**"Permission denied" on macOS/Linux**
```bash
pip3 install --user streamlit pandas numpy matplotlib seaborn scipy google-genai openpyxl
```

**Excel files not working**
```bash
pip install openpyxl xlrd
```

**Voice features not working**
```bash
# On Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
pip install speechrecognition pyttsx3

# On macOS
brew install portaudio
pip install speechrecognition pyttsx3
```

## 📈 Version History

### v2.0 (Current)
- Gemini Live AI assistant
- Professional data cleaning
- Excel file support
- Enhanced user interface

### v1.5
- Basic AI integration
- Data visualization
- CSV export functionality

### v1.0
- Initial release
- Basic EDA capabilities
- CSV file support

## 🤝 Support & Community

### Get Help
- **Documentation**: See SETUP.md for detailed instructions
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: support@datasage-ai.com

### Contributing
1. Fork the repository
2. Create feature branch
3. Make your changes
4. Submit pull request

## 📄 License

MIT License - Free for personal and commercial use

---

**Ready to analyze your data with AI?** Choose your preferred download option above and start exploring your data in minutes!

*DataSage AI - Professional data analysis made simple*