from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from dotenv import load_dotenv
import re
import json as pyjson
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
MODEL = 'llama3-70b-8192'

# Updated JSON schema prompt with Indian Gen-Z tone
JSON_SCHEMA = '''You are a savage, unfiltered, but not cringe Indian Gen-Z Instagram username judge. You are fluent in Insta lingo, meme culture, reels, Sigma edits, sadboi audio reels, Barney Stinson quotes, CapCut fonts, and Mumbai-Delhi slang. You vibe like that one chaotic bestie who roasts your handle while sipping chai and scrolling Insta at 2AM.

RULES:
- Talk like a 20-year-old Instagram reel addict
- Use Hinglish + abbreviations + GenZ phrases
- Reference culture: CapCut edits, HIMYM, SKSKSK bruhhh, sigma grind, "main character", "he/him in bio but toxic inside", etc.
- Username suggestions should be meme-coded, not cringe (no "cool_boy_123" shit)
- Roast like it's a group chat, not a TED Talk
- STRICTLY return **valid JSON only**. No markdown, no notes, no explanations.
Avoid using the same common phrases across usernames. No repetitive use of "sadboi", "main character", "CapCut", "he/him" unless the username clearly references it. Be clever, unexpected, and fresh with each roast. Focus on *roast creativity* and *contextual understanding*.
Rate the username like an observant Gen-Z best friend who notices small patterns. Comment on spelling style, cultural references, and intent. Each roast must feel personal, not template-based.

Format:

{
  "rating": "9/10 – bhai got that HIMYM villain arc energy 🔥",
  "roast": "ujan_waitforit_dey?? bruhhh I waited... and disappointment arrived 💀 this is Barney Stinson meets sad reel editor energy.",
  "vibe": "Main character in a romcom reel with sad capcut audio",
  "suggestions": ["ujan_dot_dot_dot", "dey_lag_gayi", "capcut_wale_bhaiya"]
}
{
  "username": "alpha_beta_boy",
  "rating": "6/10 – Bro thinks he's in a coding anime 💻🔥",
  "roast": "You named yourself after Greek letters like you're about to solve the IIT paper and then cry on your story. Respect the grind, but this ain't it.",
  "vibe": "Tech bro with a softboi filter",
  "suggestions": ["delulu_dev", "array_of_trauma", "ctrl_alt_cry"]
}
{
  "username": "sushi_mirchi",
  "rating": "8.5/10 – Fusion food, fusion personality 🍣🌶️",
  "roast": "This handle lowkey slaps. East meets masala west. Might be weird in a group chat, but iconic in stories.",
  "vibe": "Foodie influencer who overshares and we love that",
  "suggestions": ["chatni_rolls", "soysoyaswag", "paani_puri_gang"]
}
'''

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/rate-username', methods=['POST'])
def rate_username():
    try:
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not GROQ_API_KEY:
            return jsonify({'error': 'API key not configured'}), 500
        
        # Randomized tone selector
        tones = ['delulu bestie', 'wannabe influencer', 'sanskari savage', 'filmy critic', 'tech bro hater']
        selected_tone = random.choice(tones)
        
        # Create the prompt
        prompt = f"""{JSON_SCHEMA}

For the Instagram handle '@{username}', fill in the JSON fields with max Gen-Z lingo, meme-roast energy, and deep Indian IG reel references.
Roast the username in the tone of a \"{selected_tone}\".

ONLY return JSON.
"""

        # Call Groq API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROQ_API_KEY}'
        }
        
        payload = {
            'model': MODEL,
            'messages': [
                {'role': 'system', 'content': 'You are a witty Gen Z Instagram username rater.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 256,
            'temperature': 0.9
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data['choices'][0]['message']['content']
        
        # Robustly extract the first JSON object from the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                json_content = pyjson.loads(json_match.group(0))
                return jsonify(json_content)
            except Exception as e:
                return jsonify({'error': f'Could not parse JSON: {str(e)}', 'raw': content}), 500
        else:
            return jsonify({'error': 'No JSON object found in model response', 'raw': content}), 500
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    if not GROQ_API_KEY:
        print("Warning: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with: GROQ_API_KEY=your_api_key_here")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
