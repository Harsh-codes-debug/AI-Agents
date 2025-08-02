# DataSage AI - Complete Setup Guide

## Quick Start (Replit)

1. **Fork this Repl** or click "Use Template"
2. **Add your API key** in Secrets:
   - Go to Tools → Secrets
   - Add key: `GEMINI_API_KEY`
   - Get your free key from: https://makersuite.google.com/app/apikey
3. **Click Run** - Everything is pre-configured!
4. **Open the app** at the provided URL (usually port 5000)

## Local Installation

### Prerequisites
- Python 3.11 or higher
- Git (optional)

### Step 1: Get the Code
```bash
# Option A: Clone from repository
git clone <your-repository-url>
cd datasage-ai

# Option B: Download ZIP and extract
```

### Step 2: Install Dependencies
```bash
# Using pip (recommended)
pip install streamlit pandas numpy matplotlib seaborn scipy google-genai speechrecognition pyttsx3 reportlab weasyprint openpyxl

# Or install one by one if needed
pip install streamlit
pip install pandas numpy matplotlib seaborn scipy
pip install google-genai
pip install speechrecognition pyttsx3
pip install reportlab weasyprint openpyxl
```

### Step 3: Set up Environment Variables
```bash
# Option A: Set environment variable (Linux/Mac)
export GEMINI_API_KEY="your_api_key_here"

# Option B: Set environment variable (Windows)
set GEMINI_API_KEY=your_api_key_here

# Option C: Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### Step 4: Run the Application
```bash
streamlit run app.py --server.port 5000
```

### Step 5: Access the App
Open your browser and go to: `http://localhost:5000`

## Features Overview

### 🤖 Gemini Live AI Assistant
- Real-time streaming responses
- Natural conversation interface
- Contextual memory across chat sessions
- Proactive suggestions based on your data
- Voice-style interaction patterns

### 📊 Data Analysis Tools
- Automated Exploratory Data Analysis (EDA)
- Interactive visualizations
- Natural language querying
- Data quality assessment
- Statistical analysis

### 📤 Export Options
- CSV data export
- Excel workbooks with multiple sheets
- Professional PDF reports with charts
- Comprehensive analysis summaries

## Usage Instructions

### 1. Upload Your Data
- Click "Upload a CSV file" in the sidebar
- Or use "Load Demo Dataset" to try with sample data
- Supported formats: CSV files up to 200MB

### 2. Explore with AI
- Go to the "🤖 AI Assistant" tab
- Start a conversation: "Hey, what's interesting about this data?"
- Use quick actions: "🔍 Deep Analysis", "📊 Data Story"
- Ask natural questions like a colleague

### 3. Generate Insights
- Use the streaming AI responses for real-time analysis
- Get proactive suggestions based on your data characteristics
- Analyze patterns, trends, and business implications
- Receive data cleaning and improvement recommendations

### 4. Create Visualizations
- Go to "📊 Visualizations" tab
- Choose chart types or let AI auto-select
- Generate publication-ready plots
- Export charts for presentations

### 5. Export Results
- Go to "📤 Export" tab
- Download cleaned data as CSV or Excel
- Generate comprehensive PDF reports
- Share findings with stakeholders

## API Key Setup

### Getting a Free Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with "AI...")
5. Add it to your environment variables or Replit Secrets

### API Key Security
- Never share your API key publicly
- Don't commit it to version control
- Use environment variables or secure secret storage
- Regenerate if compromised

## Troubleshooting

### Common Issues

**"AI Assistant unavailable" message**
- Check that GEMINI_API_KEY is set correctly
- Verify your API key is valid at Google AI Studio
- Ensure you have internet connectivity

**Large file upload errors**
- Files over 200MB may cause issues
- Try data sampling for initial analysis
- Consider breaking large datasets into smaller chunks

**Voice features not working**
- Voice features work best in local environments
- Cloud deployments may have limited audio support
- Use the text chat interface for full functionality

**Charts not displaying**
- Ensure matplotlib backend is properly configured
- Check for sufficient memory for large datasets
- Try simpler chart types first

### Performance Tips

**For Large Datasets (>10MB)**
- Use data sampling for initial exploration
- Focus on key columns for analysis
- Consider data aggregation before upload

**For Better AI Responses**
- Be specific in your questions
- Provide context about your analysis goals
- Use the conversation history to build context

**For Faster Loading**
- Close unused browser tabs
- Use modern browsers (Chrome, Firefox, Safari)
- Ensure stable internet connection

## System Requirements

### Minimum Requirements
- **RAM**: 4GB (8GB recommended for large datasets)
- **Storage**: 2GB free space
- **Python**: 3.11 or higher
- **Browser**: Modern web browser with JavaScript enabled

### Recommended Setup
- **RAM**: 8GB+ for datasets over 50MB
- **CPU**: Multi-core processor for faster processing
- **Internet**: Stable connection for AI features
- **Display**: 1920x1080 or higher resolution

## File Structure

```
datasage-ai/
├── app.py                      # Main Streamlit application
├── demo_data.csv              # Sample employee dataset
├── SETUP.md                   # This setup guide
├── README.md                  # Project overview
├── replit.md                  # Technical documentation
├── dependencies.txt           # Python package list
├── pyproject.toml            # Project configuration
├── assets/
│   └── dark_mode.css         # Custom styling
└── modules/
    ├── __init__.py           # Module initialization
    ├── eda.py                # Exploratory Data Analysis
    ├── chart_gen.py          # Chart generation
    ├── query_parser.py       # Natural language queries
    ├── ai_assistant_gemini.py # Traditional AI assistant
    ├── gemini_live.py        # Gemini Live AI assistant
    ├── voice_handler.py      # Voice processing
    └── export.py             # Data export functionality
```

## Advanced Configuration

### Custom Styling
- Modify `assets/dark_mode.css` for custom themes
- Adjust colors, fonts, and layout
- Create light/dark mode variants

### AI Model Settings
- Model: `gemini-2.5-flash` (optimized for speed)
- Temperature: 0.7-0.8 (balanced creativity/accuracy)
- Max tokens: 2048 (sufficient for detailed responses)

### Performance Tuning
- Adjust `max_output_tokens` in `gemini_live.py`
- Modify streaming chunk size for response speed
- Configure memory limits for large datasets

## Deployment Options

### Replit (Recommended for beginners)
- Automatic dependency management
- Built-in secrets management
- One-click deployment
- Free tier available

### Streamlit Cloud
- Connect GitHub repository
- Automatic deployments on push
- Built-in secrets management
- Free for public repositories

### Local Server
- Full control over environment
- Better performance for large datasets
- Voice features work optimally
- Requires manual setup and maintenance

### Docker (Advanced)
- Containerized deployment
- Consistent environment across systems
- Scalable for production use
- Requires Docker knowledge

## Support & Updates

### Getting Help
- Check the troubleshooting section above
- Review error messages in the Streamlit interface
- Test with the demo dataset first
- Ensure all dependencies are installed correctly

### Updating the Application
- Pull latest changes from repository
- Update dependencies if needed
- Check for new features in README.md
- Review breaking changes in release notes

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests with clear descriptions
- Follow existing code style and structure

---

**Ready to analyze your data with AI?** Start by uploading a CSV file or trying the demo dataset!

*DataSage AI - Making data analysis accessible to everyone*