
from flask import Flask, request, jsonify
import openai
import uuid
import json
import os
from utils import get_next_question, save_session_log

#Tessaris tooolchain
#dynamic assessment bot

app = Flask(__name__)
SESSIONS = {}

@app.route("/start", methods=["POSTs"])
def start():



    # Check for OPENAI_API_KEY in environment variables and exit if not found
    open_ai_api_key = os.getenv('OPENAI_API_KEY')
    if not open_ai_api_key:
        raise EnvironmentError("Missing environment variable: 'OPENAI_API_KEY'")


    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {
        "answers": [],
        "log": []
    }

    question = get_next_question([], [])
    return jsonify({"session_id": session_id, "question": question})


@app.route("/next", methods=["POST"])
def next_question():
    data = request.get_json()
    session_id = data.get("session_id")
    answer = data.get("answer")

    if session_id not in SESSIONS:
        return jsonify({"error": "Invalid session_id"}), 400

    SESSIONS[session_id]["answers"].append(answer)
    SESSIONS[session_id]["log"].append({"answer": answer})

    question = get_next_question(SESSIONS[session_id]["answers"], SESSIONS[session_id]["log"])
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
    app.run(debug=True)
