
import openai
import json
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

SYSTEM_PROMPT = """
You are an expert AI consultant conducting a step-by-step assessment to evaluate a company's preparedness and pain points related to AI, automation, data handling, and knowledge management. 

Ask one question at a time, adapting your next question based on the answers provided so far. Keep each question clear, simple, and answerable via:
- a scale from 1 to 10,
- a short multiple-choice list (3–5 options), or
- short text (only when absolutely necessary).

Prioritize identifying bottlenecks or inefficiencies in:
- process automation,
- access to internal knowledge,
- handling of structured/unstructured data,
- workflow integration,
- decision-making support,
- document search,
- AI readiness.

Keep a professional tone, and avoid repeating earlier questions.
"""

def get_next_question(answers, logs):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for i, answer in enumerate(answers):
        messages.append({"role": "user", "content": f"My answer to question {i+1} is: {answer}"})
    
    messages.append({"role": "user", "content": "What is the next question I should answer?"})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

def save_session_log(session_id, session_data):
    log_entry = {
        "session_id": session_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": session_data
    }
    with open("assessment_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
