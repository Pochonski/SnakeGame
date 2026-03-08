from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Simple in-memory leaderboard for Vercel
leaderboard = []

@app.route('/')
def index():
    """Simple index page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Snake Game</title>
        <meta charset="utf-8">
        <style>
            body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
            h1 { color: #333; }
            .game-info { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐍 Snake Game</h1>
            <div class="game-info">
                <h2>Controls:</h2>
                <p><strong>Arrow Keys or WASD:</strong> Move snake</p>
                <p><strong>Space:</strong> Pause/Resume</p>
                <p><strong>R:</strong> Restart game</p>
                <p><strong>A:</strong> Toggle autoplay</p>
            </div>
            <div class="game-info">
                <h2>Game Features:</h2>
                <p>• Classic snake gameplay</p>
                <p>• Autoplay mode with AI</p>
                <p>• Leaderboard system</p>
                <p>• Responsive design</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the current leaderboard"""
    return jsonify({"entries": leaderboard})

@app.route('/api/score', methods=['POST'])
def submit_score():
    """Submit a new score"""
    try:
        from flask import request
        
        data = request.get_json()
        name = str(data.get('name', '')).strip()
        score = data.get('score', 0)
        
        if not name:
            return jsonify({"error": "El nombre es obligatorio."}), 400
            
        try:
            score_value = max(0, int(score))
        except (TypeError, ValueError):
            return jsonify({"error": "La puntuación debe ser numérica."}), 400
        
        # Update if it's a better score
        current_best = 0
        for entry in leaderboard:
            if entry.get('name') == name:
                current_best = entry.get('score', 0)
                break
        
        if score_value > current_best:
            # Remove existing entry for this name
            global leaderboard
            leaderboard = [entry for entry in leaderboard if entry.get('name') != name]
            
            # Add new entry
            new_entry = {
                'name': name,
                'score': score_value
            }
            leaderboard.append(new_entry)
            
            # Sort and keep top 10
            leaderboard.sort(key=lambda x: x['score'], reverse=True)
            leaderboard = leaderboard[:10]
        
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Snake Game API is running'})

# Vercel handler
def handler(environ, start_response):
    """Main handler for Vercel serverless functions"""
    return app(environ, start_response)
