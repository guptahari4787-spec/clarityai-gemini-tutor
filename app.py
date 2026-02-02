import os
import re
import json
import io
from datetime import datetime

from flask import Flask, request, session, render_template_string, send_file
import google.generativeai as genai


# ---------------- JSON EXTRACTION ----------------
def extract_json(text):
    if not text:
        return None

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None

    return None


# ---------------- CONFIG ----------------
app = Flask(__name__)
app.secret_key = "clarityai-learning-system"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")


# ---------------- LEARNING STATE ----------------
def init_learning_state():
    if "state" not in session:
        session["state"] = {
            "attempts": 0,
            "history": [],
            "mastery": 0.0,
            "trajectory": "Not started"
        }


def update_learning(confidence):
    state = session["state"]
    state["attempts"] += 1
    state["history"].append(confidence)

    state["mastery"] = round(
        sum(state["history"]) / len(state["history"]) * 100, 1
    )

    if len(state["history"]) >= 2:
        delta = state["history"][-1] - state["history"][-2]
        if delta > 0.05:
            state["trajectory"] = "Improving"
        elif delta < -0.05:
            state["trajectory"] = "Regressing"
        else:
            state["trajectory"] = "Stable"


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    init_learning_state()

    packet = session.get("packet")
    error = None

    if request.method == "POST":
        user_input = request.form.get("question", "").strip()

        if user_input:
            prompt = f"""
You are an expert human educator designing a learning experience — not answering a chat.

Your task is to:
1) Precisely diagnose why the student is confused
2) Teach in a way that feels clear, intuitive, and memorable
3) Maintain professional instructional quality suitable for judges and real learners

Respond ONLY in valid JSON.
No markdown. No explanations outside JSON.

CRITICAL STYLE RULES:

MISCONCEPTION (Diagnosis):
- Formal, validating, and precise
- 2–3 lines
- NO emojis

TEACHING STRATEGY:
- One short sentence
- Sounds like a confident tutor’s plan

ANALOGY / STEPS / EXAMPLE:
- Human, intuitive, teacher-like
- 1–2 light emojis max per view
- 3–5 lines each
- Not robotic, not childish

FORMAL VIEW:
- Concise, academic
- NO emojis

REQUIRED JSON SCHEMA:
{{
  "misconception": {{
    "id": "short_unique_id",
    "summary": "2–3 lines explaining the misunderstanding clearly"
  }},
  "strategy": "short teaching strategy name",
  "confidence_score": 0.0,
  "views": {{
    "analogy": "intuitive analogy explanation",
    "steps": ["step 1", "step 2", "step 3"],
    "example": "worked or concrete example",
    "formal": "optional concise formal explanation"
  }}
}}

STUDENT INPUT:
{user_input}
"""




            raw = model.generate_content(prompt).text.strip()
            data = extract_json(raw)

            if not data:
                error = "The AI response could not be parsed. Please try again."
            else:
                session["packet"] = data
                update_learning(data.get("confidence_score", 0.0))
                packet = data

    return render_template_string(
        TEMPLATE,
        packet=packet,
        state=session["state"],
        error=error
    )


@app.route("/export")
def export():
    output = json.dumps({
        "learning_state": session.get("state"),
        "last_packet": session.get("packet"),
        "exported_at": datetime.utcnow().isoformat()
    }, indent=2)

    return send_file(
        io.BytesIO(output.encode()),
        mimetype="application/json",
        as_attachment=True,
        download_name="clarityai_learning_summary.json"
    )


# ---------------- UI TEMPLATE ----------------
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>ClarityAI – Learning System</title>
<style>
body { margin:0; font-family:Inter, Arial; background:#f4f6f9; color:#222; }
nav { background:#1f2937; color:white; padding:14px 24px; display:flex; justify-content:space-between; }
nav span { font-weight:600; }
.container { display:flex; padding:24px; gap:24px; }
.panel { background:white; border-radius:10px; padding:20px; box-shadow:0 8px 20px rgba(0,0,0,0.06); }
.left { width:260px; }
.main { flex:1; }
.metric { margin-bottom:12px; }
.metric b { display:block; }
input, textarea, button { width:100%; padding:10px; margin-top:8px; border-radius:6px; border:1px solid #ccc; }
button { background:#2563eb; color:white; border:none; cursor:pointer; }
button:hover { background:#1d4ed8; }
.controls button { width:auto; margin-right:8px; }
#view { margin-top:16px; animation:fade .3s; }
@keyframes fade { from{opacity:0;} to{opacity:1;} }
.judge { background:#111827; color:#e5e7eb; padding:12px; border-radius:8px; margin-top:16px; display:none; }
.toggle { background:#6b7280; margin-top:10px; }
.error { background:#fee2e2; color:#991b1b; padding:10px; border-radius:6px; margin-top:10px; }
</style>
</head>
<body>

<nav>
  <span>🧠 ClarityAI</span>
  <a href="/export" style="color:white;text-decoration:none;">Export</a>
</nav>

<div class="container">

<div class="panel left">
  <h3>Learning State</h3>
  <div class="metric"><b>Attempts</b>{{ state.attempts }}</div>
  <div class="metric"><b>Mastery</b>{{ state.mastery }}%</div>
  <div class="metric"><b>Trajectory</b>{{ state.trajectory }}</div>
  <button class="toggle" onclick="toggleJudge()">Judge Mode</button>
</div>

<div class="panel main">
  <form method="post">
    <textarea name="question" rows="3" placeholder="Describe what you're confused about..."></textarea>
    <button type="submit">Analyze</button>
  </form>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  {% if packet %}
    <hr>
    <h3>Detected Misconception</h3>
    <p>{{ packet.misconception.summary }}</p>

    <h4>Teaching Strategy</h4>
    <p>{{ packet.strategy }}</p>

    <div class="controls">
      <button onclick="show('analogy')">Analogy</button>
      <button onclick="show('steps')">Steps</button>
      <button onclick="show('example')">Example</button>
      <button onclick="show('formal')">Formal</button>
    </div>

    <div id="view"></div>

    <div class="judge" id="judge">
      <h4>Judge Insight</h4>
      <p><b>Misconception ID:</b> {{ packet.misconception.id }}</p>
      <p><b>Confidence Score:</b> {{ packet.confidence_score }}</p>
      <p>
  Gemini is called once to generate a <b>Pedagogical Diagnostic Packet (PDP)</b>,
  which captures the learner’s misconception, teaching strategy, confidence score,
  and multiple explanation views.  
  The PDP is then reused across the interface without re-calling the model.
</p>

    </div>
  {% endif %}
</div>

</div>

<script>
const views = {{ packet.views | tojson if packet else {} }};
function show(v){
  const box = document.getElementById("view");
  const c = views[v];
  if(Array.isArray(c)){
    box.innerHTML = "<ul>" + c.map(x=>"<li>"+x+"</li>").join("") + "</ul>";
  } else {
    box.innerHTML = "<p>"+c+"</p>";
  }
}
function toggleJudge(){
  const j = document.getElementById("judge");
  j.style.display = j.style.display === "none" ? "block" : "none";
}
</script>

</body>
</html>
"""


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
