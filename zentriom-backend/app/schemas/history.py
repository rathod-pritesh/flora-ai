from pydantic import BaseModel
from datetime import datetime

class HistoryResponse(BaseModel):
    id: int
    
    category: str
    
    title: str
    
    input_text: str
    
    output_text: str
    
    created_at: datetime
    
    class Config:
        from_attributes: True