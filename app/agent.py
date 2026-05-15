from dotenv import load_dotenv
load_dotenv()
from typing import TypedDict, List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from datasets import Dataset
class PlannerState(TypedDict):
    question: str
    documents: List[tuple]
    relevant: bool
    answer: str
    evaluation_scores: dict
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(
        collection_name="student_docs",
        embedding_function=embeddings,
        persist_directory="../data/chromadb"
    )
SIMILARITY_THRESHOLD = 1.2
llm = ChatGroq(model_name="llama-3.3-70b-versatile")
def retrieve(state: PlannerState) -> dict:
    results = db.similarity_search_with_score(state["question"], k=3)
    documents = [(doc.page_content, score) for doc, score in results]
    if not documents:
        return {"documents": [], "answer": "No relevant data found in the PDF. Please refer to another source."}
    return {"documents": documents}

# conditional function — reads state, returns string
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
    response = llm.invoke(prompt)
    return {"answer": response.content}
def route(state: PlannerState) -> str:
    if state["relevant"]:
        return "generate"
    return END
def evaluate_node(state: PlannerState) -> PlannerState:
    question = state["question"]
    answer = state["answer"]
    documents = state["documents"]

    # Extract plain string contexts from tuples
    contexts = []
    for doc in documents:
        if isinstance(doc, tuple):
            contexts.append(doc[0])
        else:
            contexts.append(doc)

    # Build HuggingFace Dataset
    data = {
        "question": [question],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": [""]
    }
    dataset = Dataset.from_dict(data)

    # Tell RAGAS to use Groq instead of OpenAI
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper

    ragas_llm = LangchainLLMWrapper(llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

    # Run RAGAS evaluation with Groq
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ],
        llm=ragas_llm,
        embeddings=ragas_embeddings
    )

    # Convert to plain dict and store in state
    # With this
    import math
    raw_scores = result.to_pandas().to_dict(orient="records")[0]
    clean_scores = {
        k: (None if isinstance(v, float) and math.isnan(v) else v)
        for k, v in raw_scores.items()
     }
    state["evaluation_scores"] = clean_scores
    return state
workflow= StateGraph(PlannerState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_relevance", grade_relevance)
workflow.add_node("generate", generate)
workflow.add_node("evaluate", evaluate_node)
workflow.set_entry_point("retrieve")
workflow.add_conditional_edges("retrieve",check_docs,{"end": END, "grade_relevance":"grade_relevance"})
workflow.add_conditional_edges("grade_relevance",route)
workflow.add_edge("generate","evaluate")
workflow.add_edge("evaluate", END)
planner_graph=workflow.compile()
