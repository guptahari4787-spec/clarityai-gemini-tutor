# ClarityAI — Pedagogical Learning System

ClarityAI is a learning system that diagnoses *why* a learner is confused and
teaches concepts the way a skilled human tutor would — by separating
**misconception diagnosis** from **instruction**.

This project was built for the **Gemini 3 Hackathon**.

---

## 🧠 Core Idea (What makes this different)

Most AI tutors behave like chatbots:  
they generate a new explanation every time you ask.

**ClarityAI does not.**

ClarityAI uses Gemini **once per question** to generate a structured
**Pedagogical Diagnostic Packet (PDP)**, which contains:

- Detected misconception
- Teaching strategy
- Confidence score
- Multiple teaching views (Analogy, Steps, Example, Formal)

That single packet is then reused across the UI **without re-calling Gemini**.

This mirrors how real educators teach:
> Diagnose first. Teach second. Reinforce from multiple angles.

---

## ✨ Key Features

- 🔍 **Misconception-first learning**
- 🧠 **Single Gemini call per concept**
- 🔁 **Multi-view explanations without extra API calls**
- 📈 **Learning trajectory & mastery tracking**
- 🧑‍⚖️ **Judge-only insight mode**
- 📤 **Exportable learning summary**

This system works for **any conceptual confusion** — not just coding  
(math, physics, theory, abstract ideas, etc.).

---

## 🏗️ Architecture (High-level)

1. User submits what they are confused about
2. Gemini generates a **Pedagogical Diagnostic Packet (JSON)**
3. Packet is cached in session
4. UI switches between views locally (no more AI calls)
5. Learning state updates across attempts

This keeps the system:
- Efficient
- Transparent
- Scalable

---

## 🔧 Tech Stack

- **Python**
- **Flask**
- **Google Gemini 3 API**
- HTML / CSS / JavaScript
- Session-based state tracking

---

## ▶️ How to Run Locally (Optional)

> Judges are **not required** to run this locally.
> The demo video explains the full flow.

### 1. Install dependencies
```bash
pip install flask google-generativeai
