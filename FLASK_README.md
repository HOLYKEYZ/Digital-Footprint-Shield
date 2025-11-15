FOR CONTRIBUTORS ONLY!!!

# Flask Web Interface - Digital Footprint Shield

## Overview

The Flask web interface provides a user-friendly web application for Digital Footprint Shield, allowing users to scan their privacy exposure through a modern web browser.

## Features

- 🖥️ **Web Interface**: Clean, modern dark mode interface
- 📝 **Input Form**: Easy-to-use form for entering name, email, or username
- 🔍 **Real-time Scanning**: Performs web search, breach checking, and risk analysis
- 📊 **Results Display**: Color-coded risk scores and detailed breakdowns
- 💡 **AI Recommendations**: Actionable privacy improvement tips
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Installation

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   - Edit `config.txt` with your API keys, or
   - Set environment variables:
     ```bash
     set GOOGLE_API_KEY=your_api_key
     set GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
     ```

## Running the Application

### Development Mode

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Production Mode

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage

1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Enter Information**: Fill in name, email, or username (at least one required)
3. **Start Scan**: Click "Start Scan" button
4. **View Results**: Results will be displayed with:
   - Risk score (color-coded: green/yellow/red)
   - Web search results
   - Breach detection
   - Privacy recommendations


## License

Same as the main Digital Footprint Shield project.
