from pydantic import BaseModel

class LeaveOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
