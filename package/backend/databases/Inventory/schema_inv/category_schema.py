from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel
from pydantic.types import StringConstraints


class CategoryCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=150)]

    description: Optional[str] = None
    status: Annotated[str, StringConstraints(pattern="^(active|inactive)$")] = "active"


# Schema for returning data to client
class CategoryOut(CategoryCreate):
    category_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
