from fastapi import APIRouter
from pydantic import BaseModel

from app.graphs.workflow import graph

router = APIRouter()

class AIRequest(BaseModel):
    task: str
    prompt: str
    
@router.post("/ai")
def ai(request: AIRequest):
    
    result = graph.invoke({
        "task": request.task,
        "prompt": request.prompt
    })
    
    return {
        "response": result["result"]
    }