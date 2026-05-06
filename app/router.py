from fastapi import APIRouter
from pydantic import BaseModel
from agent import planner_graph

router = APIRouter(prefix="/api", tags=["planner"])

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask(request: AskRequest):
    result = planner_graph.invoke({"question": request.question})
    return {"answer": result["answer"]}