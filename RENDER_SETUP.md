# Render Deployment Setup

## Required Environment Variables

Set these environment variables in your Render dashboard:

### Required Variables

1. **GOOGLE_API_KEY**
   - Your Google Custom Search API key
   - Get it from: https://console.cloud.google.com/
   - Required for web search functionality

2. **CSE_ID**
   - Your Google Custom Search Engine ID
   - Get it from: https://programmablesearchengine.google.com/
   - Required for web search functionality

### Optional Variables

3. **HIBP_API_KEY**
   - HaveIBeenPwned API key (optional but recommended)
   - Get it from: https://haveibeenpwned.com/API/Key
   - Provides higher rate limits for breach checking

4. **GROK_API_KEY**
   - Grok API key for AI-powered recommendations (optional)
   - Get it from: https://x.ai/ or https://docs.x.ai/
   - Enables AI-powered privacy recommendations

## Setting Environment Variables on Render

1. Go to your Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add each environment variable:
   - Key: `GOOGLE_API_KEY`
   - Value: `your_google_api_key_here`
5. Repeat for `CSE_ID` and optional keys
6. Save and redeploy

## Important Notes

- **No fallback to gist**: The application will fail to start if required environment variables are missing
- **Security**: Never commit API keys to version control
- **Validation**: The app validates environment variables on startup and will show clear error messages if missing

