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



# this is the marshmello version
#  switch if u want 

'''
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    role = fields.Str(load_default="user")
    created_at = fields.DateTime(required=True)

class UserListSchema(Schema):
    items = fields.List(fields.Nested(UserSchema), required=True)
    pagination = fields.Dict(required=True)


'''


#✅ Schema instances (Marshmallow-style)
"""
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_list_schema = UserListSchema()
"""