import os
from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from openai import OpenAI
from langgraph.graph import StateGraph, END

class PlannerState(TypedDict):
    question: str
    documents: List[tuple]
    relevant: bool
    answer: str

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(
    collection_name="student_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

SIMILARITY_THRESHOLD = 1.2
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def retrieve(state: PlannerState) -> dict:
    results = db.similarity_search_with_score(state["question"], k=3)
    documents = [(doc.page_content, score) for doc, score in results]
    print(f"DEBUG scores: {[score for _, score in documents]}", flush=True)
    if not documents:
        return {"documents": [], "answer": "No relevant data found in the PDF."}
    return {"documents": documents}

def check_docs(state: PlannerState) -> str:
    if len(state["documents"]) == 0:
        return "end"
    return "grade_relevance"

def grade_relevance(state: PlannerState) -> dict:
    for text, score in state["documents"]:
        if score < SIMILARITY_THRESHOLD:
            return {"relevant": True}
    return {"relevant": False}

def generate(state: PlannerState) -> dict:
    context = "\n\n".join([text for text, score in state["documents"]])
    prompt = f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {state['question']}"

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": response.choices[0].message.content}

def route(state: PlannerState) -> str:
    if state["relevant"]:
        return "generate"
    return END

workflow = StateGraph(PlannerState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_relevance", grade_relevance)
workflow.add_node("generate", generate)
workflow.set_entry_point("retrieve")
workflow.add_conditional_edges("retrieve", check_docs, {"end": END, "grade_relevance": "grade_relevance"})
workflow.add_conditional_edges("grade_relevance", route)
workflow.add_edge("generate", END)
planner_graph = workflow.compile()