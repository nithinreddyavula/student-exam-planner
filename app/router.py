from fastapi import APIRouter
from pydantic import BaseModel
from agent import planner_graph

router = APIRouter(prefix="/api", tags=["planner"])

class AskRequest(BaseModel):
    question: str

@router.post("/ask")

async def ask(request: AskRequest):
    try:
        result = planner_graph.invoke({"question": request.question})
        answer = result.get("answer", "")

        if not answer:
            return {"answer": "No relevant data found. Please refer to another source."}

        return {"answer": answer}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing your request."
        )
    