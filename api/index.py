import json
from threading import Lock
from typing import Dict, List

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Almacenamiento en memoria para Vercel (no permite escritura de archivos)
_leaderboard_data = {}
_leaderboard_lock = Lock()


def _load_leaderboard() -> Dict[str, int]:
    return _leaderboard_data.copy()


def _save_leaderboard(entries: Dict[str, int]) -> None:
    global _leaderboard_data
    _leaderboard_data = entries.copy()


def _sorted_entries(entries: Dict[str, int]) -> List[Dict[str, int]]:
    return [
        {"name": name, "score": score}
        for name, score in sorted(entries.items(), key=lambda item: item[1], reverse=True)
    ]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    with _leaderboard_lock:
        entries = _sorted_entries(_load_leaderboard())
    return jsonify({"entries": entries})


@app.route("/api/score", methods=["POST"])
def submit_score():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    score = payload.get("score")

    if not name:
        return jsonify({"error": "El nombre es obligatorio."}), 400

    try:
        score_value = max(0, int(score))
    except (TypeError, ValueError):
        return jsonify({"error": "La puntuación debe ser numérica."}), 400

    with _leaderboard_lock:
        leaderboard = _load_leaderboard()
        current_best = leaderboard.get(name, 0)
        if score_value > current_best:
            leaderboard[name] = score_value
            _save_leaderboard(leaderboard)
        entries = _sorted_entries(leaderboard)

    return jsonify({"status": "ok", "entries": entries})


# Handler para Vercel
def handler(environ, start_response):
    return app(environ, start_response)
