from datetime import datetime

from pydantic import BaseModel, EmailStr, UUID4


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str


class UserResponse(UserBaseSchema):
    id: UUID4
    created_at: datetime
    updated_at: datetime
