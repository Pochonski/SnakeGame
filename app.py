import json
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DATA_FILE = Path("leaderboard.json")
_leaderboard_lock = Lock()


def _load_leaderboard() -> dict[str, int]:
    if not DATA_FILE.exists():
        return {}

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(name): int(score) for name, score in data.items()}
    except (json.JSONDecodeError, ValueError):
        pass

    return {}


def _save_leaderboard(entries: dict[str, int]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as fp:
        json.dump(entries, fp, ensure_ascii=False, indent=2)


def _sorted_entries(entries: dict[str, int]) -> list[dict[str, int]]:
    return [
        {"name": name, "score": score}
        for name, score in sorted(entries.items(), key=lambda item: item[1], reverse=True)
    ]


@app.route("/")
def index() -> str:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

































    