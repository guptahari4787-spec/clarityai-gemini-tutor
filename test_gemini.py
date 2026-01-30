import google.generativeai as genai

genai.configure(api_key="AIzaSyD8Fj32ZNtPvIdrPAeCyZHHBHw4U2Zv6m4")

model = genai.GenerativeModel("models/gemini-flash-latest")

response = model.generate_content(
    "Explain recursion in C in very simple words."
)

print(response.text)
