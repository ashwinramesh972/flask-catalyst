from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True  

class UserList(BaseModel):
    items: List[UserOut]
    pagination: dict