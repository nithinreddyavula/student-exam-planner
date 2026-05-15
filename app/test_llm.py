import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"Key: {api_key[:15]}...")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash-lite")
response = model.generate_content("What is CPU scheduling in one line?")
print(response.text)