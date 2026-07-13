from sqlalchemy.orm import Session

from app.models.ai_history import AIHistory

def save_history(
    db: Session,
    user_id: int,
    category: str,
    title: str,
    input_text: str,
    output_text: str
):
    history = AIHistory(
        user_id=user_id,
        category=category,
        title=title,
        input_text=input_text,
        output_text=output_text
    )
    
    db.add(history)
    db.commit()
    
    db.refresh(history)
    
    return history

def get_user_history(
    db: Session,
    user_id: int
):
    return (
        db.query(AIHistory)
        .filter(
            AIHistory.user_id == user_id
        )
        .order_by(
            AIHistory.created_at.desc()
        )
        .all()
    )
    
def delete_history(
    db,
    history_id: int,
    user_id: int
):
    history = (
        db.query(AIHistory)
        .filter(
            AIHistory.id == history_id,
            AIHistory.user_id == user_id
        )
        .first()
    )
    
    if not history:
        return False
    
    db.delete(history)
    db.commit()
    
    return True

def clear_history(
    db,
    user_id: int
):
    (
        db.query(AIHistory)
        .filter(
            AIHistory.user_id == user_id
        )
        .delete()
    )
    
    db.commit()
    
    return True