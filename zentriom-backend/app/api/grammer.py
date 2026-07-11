from fastapi import APIRouter
from pydantic import BaseModel

from app.graphs.workflow import graph

router = APIRouter()

class GrammerRequest(BaseModel):
    text: str

@router.post("/grammer")
def grammer(data: GrammerRequest):

    result = graph.invoke({
        "task": "grammar",
        "prompt": data.text
    })

    return {
        "corrected_text": result["result"]
    }