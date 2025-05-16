from flask import Flask, request, jsonify
import openai
import uuid
import json
import os
from utils import get_next_question, save_session_log
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Accept"])

SESSIONS = {}

@app.route("/start", methods=["POST"])
def start():
    # Check for OPENAI_API_KEY in environment variables
    open_ai_api_key = os.getenv('OPENAI_API_KEY')
    if not open_ai_api_key:
        raise EnvironmentError("Missing environment variable: 'OPENAI_API_KEY'")

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "log": []
    }

    # Get first question
    question = get_next_question([])
    SESSIONS[session_id]["log"].append({"question": question})

    return jsonify({"session_id": session_id, "question": question})


@app.route("/next", methods=["POST"])
def next_question():
    data = request.get_json()
    session_id = data.get("session_id")
    answer = data.get("answer")

    if session_id not in SESSIONS:
        return jsonify({"error": "Invalid session_id"}), 400

    session = SESSIONS[session_id]
    log = session["log"]

    # Save user's answer to the previous question
    if log and "answer" not in log[-1]:
        log[-1]["answer"] = answer
    else:
        log.append({"answer": answer})

    # Limit to 10 questions
    if len(log) >= 10:
        return jsonify({"message": "Assessment complete. Thank you!", "complete": True})

    # Get next question
    question = get_next_question(log)
    log.append({"question": question})

    return jsonify({"question": question})


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    session_id = data.get("session_id")

    if session_id not in SESSIONS:
        return jsonify({"error": "Invalid session_id"}), 400

    save_session_log(session_id, SESSIONS[session_id])
    return jsonify({"message": "Assessment complete. Thank you!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context=("cert.pem", "key.pem"))