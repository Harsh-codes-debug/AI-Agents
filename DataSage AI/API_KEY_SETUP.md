# 🔑 API Key Setup Guide for DataSage AI

## Why You Need Your Own API Key

DataSage AI uses Google's Gemini AI for intelligent data analysis. Each user needs their own free API key for security and usage tracking.

## Quick Setup (2 Minutes)

### Step 1: Get Your Free API Key
1. **Visit**: https://aistudio.google.com/app/apikey
2. **Sign in**: Use any Google account (no special setup needed)
3. **Create Key**: Click "Create API Key" button
4. **Copy**: Save the key (starts with "AIza...")

### Step 2: Add to Your Deployment

**If using Replit:**
1. Go to Secrets tab in your Replit
2. Add key: `GEMINI_API_KEY`
3. Paste your API key as the value

**If running locally:**
```bash
# Windows
set GEMINI_API_KEY=your_key_here

# Mac/Linux
export GEMINI_API_KEY=your_key_here
```

**If using Streamlit Cloud:**
1. Go to app settings
2. Add to Secrets section
3. Key: `GEMINI_API_KEY`, Value: your key

### Step 3: Test
1. Start your DataSage AI application
2. Try the AI assistant features
3. If working, you're all set!

## Free Usage Limits

Google provides generous free limits:
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per month

This is plenty for typical data analysis work.

## Security Best Practices

- Never share your API key publicly
- Don't commit keys to code repositories
- Use environment variables or secrets management
- Each person should use their own key

## Troubleshooting

**Error: "API key not found"**
- Check spelling of `GEMINI_API_KEY`
- Ensure no extra spaces in the key
- Restart your application after adding key

**Error: "Invalid API key"**
- Generate a new key from Google AI Studio
- Double-check you copied the complete key

**Error: "Quota exceeded"**
- You've hit the daily limit (rare for normal use)
- Wait 24 hours or upgrade to paid plan

## Alternative: Demo Mode

If you can't set up an API key immediately, DataSage AI will still work for:
- Data upload and preview
- Basic statistics and visualizations
- Data cleaning tools
- Export functionality

Only the AI assistant features require the API key.

---

**Ready to start?** Get your free API key and unlock the full power of AI-assisted data analysis!