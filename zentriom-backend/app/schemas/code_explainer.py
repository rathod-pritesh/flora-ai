from pydantic import BaseModel

class CodeExplainerRequest(BaseModel):
    code: str