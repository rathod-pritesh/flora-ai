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

class GrammerRequest(BaseModel):
    text: str

@router.post("/grammar")
def grammer(
    data: GrammerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = graph.invoke({
        "task": "grammar",
        "prompt": data.text
    })
    
    save_history(
        db=db,
        user_id=current_user.id,
        category="grammar",
        title="Grammar Correction",
        input_text=data.text,
        output_text=result["result"]
    )

    return {
        "corrected_text": result["result"]
    }