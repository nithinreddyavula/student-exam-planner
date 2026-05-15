import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

load_dotenv()

# Constants
CHROMA_DB_PATH = "data/chromadb"
SIMILARITY_THRESHOLD = 0.5
TOP_K_RESULTS = 3

# Module level initialization — loaded once, reused always
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def ingest_pdf(pdf_path: str) -> str:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)

    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_metadata={"hnsw:space": "cosine"}
    )

    return f"Ingested {len(chunks)} chunks from {pdf_path}"

def retrieve_answer(question: str) -> str:

    db = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )

    results = db.similarity_search_with_score(question, TOP_K_RESULTS)

    # DEBUG — remove after fixing
    for doc, score in results:
        print(f"Score: {score} | Content: {doc.page_content[:100]}")

    relevant_docs = [
        doc for doc, score in results if score <= SIMILARITY_THRESHOLD
    ]

    if not relevant_docs:
        return "I could not find relevant information in your study material for this question. Please check your notes or textbook directly."

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""You are a helpful study assistant.
Use the following context from the student's notes to answer the question.
Only use the context provided. Do not make up answers.

Context:
{context}

Question: {question}

Answer:"""

    response = llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    print("Ingesting PDF...")
    result = ingest_pdf("data/os.pdf")
    print(result)

    print("\nAsking question...")
    answer = retrieve_answer("What is operating system?")
    print(f"Answer: {answer}")