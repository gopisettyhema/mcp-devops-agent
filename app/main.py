from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import DevOpsAgent

app = FastAPI()
agent = DevOpsAgent()

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "MCP DevOps Agent Running"}

@app.post("/chat")
def chat(query: Query):
    response = agent.handle_query(query.question)
    return {"response": response}