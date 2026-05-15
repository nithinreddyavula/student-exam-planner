import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models = list(genai.list_models())

with open("models_list.txt", "w") as f:
    for m in models:
        # only save models that support generateContent
        if "generateContent" in m.supported_generation_methods:
            f.write(m.name + "\n")

print("Saved generateContent models to models_list.txt")