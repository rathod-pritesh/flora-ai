from pydantic import BaseModel

class LinkedInRequest(BaseModel):
    post_type: str
    topic: str
    experience: str
    tone: str = "professional"
    length: str