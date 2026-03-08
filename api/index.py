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

# Path to leaderboard file
LEADERBOARD_FILE = '../leaderboard.json'

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
    return jsonify(leaderboard)

@app.route('/api/leaderboard', methods=['POST'])
def update_leaderboard():
    """Update the leaderboard with a new score"""
    try:
        data = request.get_json()
        name = data.get('name', 'Anonymous')
        score = data.get('score', 0)
        
        # Load current leaderboard
        leaderboard = load_leaderboard()
        
        # Add new score
        new_entry = {
            'name': name,
            'score': score,
            'date': json.dumps({'$date': {'$numberLong': str(int(__import__('time').time() * 1000))}})
        }
        
        leaderboard.append(new_entry)
        
        # Sort by score (descending) and keep top 10
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:10]
        
        # Save updated leaderboard
        if save_leaderboard(leaderboard):
            return jsonify({'success': True, 'leaderboard': leaderboard})
        else:
            return jsonify({'success': False, 'error': 'Failed to save leaderboard'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Snake Game API is running'})

# Vercel serverless function handler
def handler(request):
    """Main handler for Vercel serverless functions"""
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    # For local development
    app.run(debug=True, port=5000)
