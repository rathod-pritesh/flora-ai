from fastapi import APIRouter, Depends
from app.services.history_service import save_history
from app.schemas.code_explainer import (
    CodeExplainerRequest
)

from app.graphs.workflow import graph

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.users import User

router = APIRouter()

@router.post("/code-explainer")
def code_explainer(
    data: CodeExplainerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = graph.invoke({
        "task": "code_explainer",
        "code": data.code,
    })
    
    save_history(
        db=db,
        user_id=current_user.id,
        category="code_explainer",
        title=f"{result['language']} Code Explanation",
        input_text=data.code,
        output_text=result["result"]
    )
    
    return {
        "language": result["language"],
        "explanation": result["result"]
    }