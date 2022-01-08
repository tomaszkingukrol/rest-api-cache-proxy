from pydantic import BaseModel

class ResponseModel(BaseModel):
    content: str
    status_code: int
    headers: dict
    media_type: str










