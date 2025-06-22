# @Roasted Username Rater 🔥

A fun Gen Z-style web app that rates Instagram usernames using AI. Built with Flask backend and vanilla frontend.

## Features

- ⭐ Rate Instagram handles out of 10 with witty comments
- 🔥 Generate funny roasts
- 🎭 Get vibe tags (like "Gymrat-in-Training", "NPC", "Softboi")
- 💡 Suggest better username alternatives
- 📱 Mobile-responsive design
- 🎨 Dark mode Instagram aesthetic

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/

### 3. Run the Application

```bash
python app.py
```

The app will be available at: http://localhost:5000

## How It Works

- **Frontend**: Pure HTML/CSS/JS with Instagram-inspired dark theme
- **Backend**: Flask server that securely handles Groq API calls
- **API**: Uses Groq's llama3-70b-8192 model for witty Gen Z responses

## File Structure

```
├── app.py              # Flask backend server
├── index.html          # Main HTML page
├── style.css           # Styling
├── script.js           # Frontend JavaScript
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── README.md          # This file
```

## Security

- API key is stored server-side in `.env` file
- Frontend never sees the API key
- All API calls go through the secure Flask backend

## Development

The Flask server runs in debug mode by default. For production, set `debug=False` in `app.py`. 