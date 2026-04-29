import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load the API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create an embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key
)

# Convert two sentences into numbers (vectors)
sentence1 = "Operating systems manage computer hardware"
sentence2 = "CPU scheduling is part of operating systems"
sentence3 = "I love eating biryani"

vec1 = embeddings.embed_query(sentence1)
vec2 = embeddings.embed_query(sentence2)
vec3 = embeddings.embed_query(sentence3)

print(f"Vector size: {len(vec1)} numbers")
print(f"\nFirst 5 numbers of sentence1: {vec1[:5]}")
print(f"First 5 numbers of sentence2: {vec2[:5]}")
print(f"First 5 numbers of sentence3: {vec3[:5]}") 
