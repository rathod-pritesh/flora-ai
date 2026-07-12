from fastapi import APIRouter, Depends

from pydantic import BaseModel

from app.services.history_service import save_history

from app.graphs.workflow import graph


from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.users import User


router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    

@router.post("/chat")
def chat(
    data: PromptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = graph.invoke({
        "task": "chat",
        "prompt": data.prompt
    })
    
    save_history(
        db=db,
        user_id=current_user.id,
        category="chat",
        title=data.prompt[:50],
        input_text=data.prompt,
        output_text=result["result"]
    )

    return {
        "response": result["result"]
    }