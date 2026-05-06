from typing import TypedDict, List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
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
SIMILARITY_THRESHOLD = 0.5
llm = ChatGroq(model_name="llama3-8b-8192")
def retrieve(state: PlannerState) -> dict:
    results = db.similarity_search_with_score(state["question"], k=3)
    documents = [(doc.page_content, score) for doc, score in results]
    return {"documents": documents}
def grade_relevance(state: PlannerState) -> dict:
    for text, score in state["documents"] :
        if score < SIMILARITY_THRESHOLD :
            return {"relevant": True}
    return {"relevant": False}
def generate(state: PlannerState) -> dict:
    context = "\n\n".join([text for text, score in state["documents"]])
    prompt = f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {state['question']}"
    response = llm.invoke(prompt)
    return {"answer": response.content}
def route(state: PlannerState) -> str:
    if state["relevant"]:
        return "generate"
    return END
workflow= StateGraph(PlannerState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_relevance", grade_relevance)
workflow.add_node("generate", generate)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve","grade_relevance")
workflow.add_conditional_edges("grade_relevance",route)
workflow.add_edge("generate",END)
app=workflow.compile()
