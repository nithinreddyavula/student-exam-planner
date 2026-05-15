from fastapi import FastAPI
from router import router

app = FastAPI(title="Student Exam Planner")
app.include_router(router)