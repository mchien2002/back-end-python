from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    image: str = ''
    email:str =''
    password: str  =''
    status: int = 1
    role: int = 1
    accessed_at = []
    created_at: datetime = datetime.now()