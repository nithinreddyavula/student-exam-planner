from fastapi import APIRouter, HTTPException
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

        return {"answer": result["answer"]}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    