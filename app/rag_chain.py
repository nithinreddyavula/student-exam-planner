import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DB_PATH = "data/chromadb"

def ingest_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)

    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )

    return f"Ingested {len(chunks)} chunks from {pdf_path}"

def retrieve_answer(question: str) -> str:
    
    embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    docs = db.similarity_search(question, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a helpful study assistant.
Use the following context from the student's notes to answer the question.
If the answer is not in the context, say 'No relevant data found.'

Context:
{context}

Question: {question}

Answer:"""

    from langchain_groq import ChatGroq

    llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
    )

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    print("Ingesting PDF...")
    result = ingest_pdf("data/sample_notes.pdf")
    print(result)

    print("\nAsking question...")
    answer = retrieve_answer("What is CPU scheduling?")
    print(f"Answer: {answer}")