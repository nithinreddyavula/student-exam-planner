from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

loader = PyPDFLoader("../data/os.pdf")
pages = loader.load()
print(f"Loaded {len(pages)} pages")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(pages)
print(f"Total chunks: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="student_docs",
    persist_directory="../data/chromadb"
)

print(f"Ingestion complete. Total documents stored: {db._collection.count()}")