from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.services.history_service import (
    get_user_history
)

from app.core.dependencies import (
    get_current_user
)

from app.models.users import User

router = APIRouter()

@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    data = get_user_history(
        db=db,
        user_id=current_user.id
    )
    
    return data