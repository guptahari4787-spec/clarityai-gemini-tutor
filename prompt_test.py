import google.generativeai as genai

genai.configure(api_key="AIzaSyD8Fj32ZNtPvIdrPAeCyZHHBHw4U2Zv6m4")

model = genai.GenerativeModel("models/gemini-flash-latest")

prompt = """
You are an expert teacher.
First, identify what the student is confused about.
Then explain the concept in 3 levels:
1) Beginner (very simple)
2) College level (with example)
3) Interview level (key points)

Student question:
Explain recursion in C.
"""

response = model.generate_content(prompt)
print(response.text)
