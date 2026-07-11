from fastapi import APIRouter
from pydantic import BaseModel

from app.services.granite import ask_granite
from app.graphs.workflow import graph

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    

@router.post("/chat")
def chat(data: PromptRequest):
    result = graph.invoke({
        "task": "chat",
        "prompt": data.prompt
    })

    return {
        "response": result["result"]
    }