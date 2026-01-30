import google.generativeai as genai

genai.configure(api_key="AIzaSyD8Fj32ZNtPvIdrPAeCyZHHBHw4U2Zv6m4")

models = genai.list_models()
for m in models:
    print(m.name)
