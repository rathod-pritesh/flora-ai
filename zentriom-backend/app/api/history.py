from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.services.history_service import (
    get_user_history,
    delete_history,
    clear_history
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

@router.delete("/history/{history_id}")
def delete_history_item(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_history(
        db=db,
        history_id=history_id,
        user_id=current_user.id
    )
    
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="History record not found"
        )
        
    return {
        "message": "History deleted successfully"
    }
    
@router.delete("/history")
def clear_all_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clear_history(
        db=db,
        user_id=current_user.id
    )
    
    return {
        "message": "All hisotry deleted successfully"
    }
    
    