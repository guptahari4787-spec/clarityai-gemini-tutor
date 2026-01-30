from flask import Flask, request, render_template_string
import google.generativeai as genai

# CONFIGURE GEMINI
genai.configure(api_key="AIzaSyD8Fj32ZNtPvIdrPAeCyZHHBHw4U2Zv6m4")
model = genai.GenerativeModel("models/gemini-flash-latest")

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gemini Confusion-to-Clarity Tutor</title>
   <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        background: #f7f9fc;
        margin: 0;
        padding: 40px;
        color: #333;
    }

    .container {
        max-width: 900px;
        margin: auto;
        background: #ffffff;
        padding: 30px 40px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }

    h1 {
        margin-top: 0;
        color: #2c3e50;
    }

    p.subtitle {
        color: #555;
        margin-bottom: 25px;
    }

    textarea {
        width: 100%;
        padding: 12px;
        font-size: 15px;
        border-radius: 8px;
        border: 1px solid #ccc;
        resize: vertical;
    }

    .levels {
        margin: 15px 0 20px 0;
    }

    .levels label {
        margin-right: 15px;
        font-weight: 500;
    }

    button {
        background: #4f46e5;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
    }

    button:hover {
        background: #4338ca;
    }

    .output {
        margin-top: 30px;
    }

    pre {
        background: #f4f6fa;
        padding: 20px;
        border-radius: 8px;
        white-space: pre-wrap;
        line-height: 1.5;
    }

    footer {
        margin-top: 40px;
        text-align: center;
        font-size: 13px;
        color: #777;
    }
</style>

</head>
<body>
    <div class="container">
        <h1>🧠 ClarityAI</h1>
        <p class="subtitle">
            From confusion to clarity — powered by Gemini
        </p>
    <p>Choose your understanding level and paste your doubt.</p>

    <form method="post">
        <div class="levels">
            <label><input type="radio" name="level" value="Beginner" checked> Beginner</label>
            <label><input type="radio" name="level" value="College"> College</label>
            <label><input type="radio" name="level" value="Interview"> Interview</label>
        </div>

        <textarea name="question" rows="8" placeholder="Explain recursion in C..."></textarea><br><br>
        <button type="submit">Analyze My Confusion</button>
    </form>

    {% if answer %}
        <h2>AI Explanation</h2>
        <pre>{{ answer }}</pre>
    {% endif %}
        <footer>
            Built with Google Gemini • Hackathon Project
        </footer>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        user_input = request.form["question"]
        level = request.form.get("level", "Beginner")

        prompt = f"""
You are an expert teacher.

First, identify what the student is confused about.

Then explain the concept strictly at **{level} level**.

Guidelines:
- Beginner: very simple language, analogy
- College: proper explanation + example
- Interview: concise, key points, pitfalls

Student question:
{user_input}
"""

        response = model.generate_content(prompt)
        answer = response.text

    return render_template_string(HTML, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
