import os
import sys
import json
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)

# Path to leaderboard file - use /tmp for Vercel
LEADERBOARD_FILE = '/tmp/leaderboard.json'

def load_leaderboard():
    """Load leaderboard from JSON file"""
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file"""
    try:
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(leaderboard, f, indent=2)
        return True
    except:
        return False

@app.route('/')
def index():
    """Serve the main game page"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('../static', filename)

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the current leaderboard"""
    leaderboard = load_leaderboard()
    return jsonify({'entries': leaderboard})

@app.route('/api/score', methods=['POST'])
def submit_score():
    """Submit a new score (matches the original app.py API)"""
    try:
        data = request.get_json()
        name = str(data.get('name', '')).strip()
        score = data.get('score', 0)
        
        if not name:
            return jsonify({"error": "El nombre es obligatorio."}), 400
            
        try:
            score_value = max(0, int(score))
        except (TypeError, ValueError):
            return jsonify({"error": "La puntuación debe ser numérica."}), 400
        
        # Load current leaderboard
        leaderboard = load_leaderboard()
        
        # Update if it's a better score
        current_best = 0
        for entry in leaderboard:
            if entry.get('name') == name:
                current_best = entry.get('score', 0)
                break
        
        if score_value > current_best:
            # Remove existing entry for this name
            leaderboard = [entry for entry in leaderboard if entry.get('name') != name]
            
            # Add new entry
            new_entry = {
                'name': name,
                'score': score_value,
                'date': json.dumps({'$date': {'$numberLong': str(int(__import__('time').time() * 1000))}})
            }
            leaderboard.append(new_entry)
            
            # Sort and keep top 10
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            leaderboard = leaderboard[:10]
            
            if not save_leaderboard(leaderboard):
                return jsonify({"error": "Failed to save leaderboard"}), 500
        
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Snake Game API is running'})

# Vercel serverless function handler
def handler(environ, start_response):
    """Main handler for Vercel serverless functions"""
    return app(environ, start_response)

if __name__ == '__main__':
    # For local development
    app.run(debug=True, port=5000)
