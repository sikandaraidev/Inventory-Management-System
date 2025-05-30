from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr
from pydantic.types import StringConstraints


class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3, max_length=150)]
    email: EmailStr
    role: Annotated[str, StringConstraints(min_length=5, max_length=50)]
    password_hash: Annotated[str, StringConstraints(min_length=5, max_length=100)]


# Schema for returning data to client
class UsertOut(UserCreate):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
