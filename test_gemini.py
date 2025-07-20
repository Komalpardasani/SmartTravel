# test_gemini_env.py

from utils.gemini_client import ask_gemini

response = ask_gemini("Suggest 3 beautiful places to visit in Japan.")
print("✅ Gemini Response:\n", response)



