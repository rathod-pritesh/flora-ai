from fastapi import APIRouter

from app.schemas.linkedin import LinkedInRequest
from app.graphs.workflow import graph

router = APIRouter()

@router.post("/linkedin")
def linkedin(data: LinkedInRequest):
    result = graph.invoke({
        "task": "linkedin",
        "post_type": data.post_type,
        "topic": data.topic,
        "experience": data.experience,
        "tone": data.tone,
        "length": data.length
    })
    return {
        "post": result["result"]
    }