from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import StringConstraints


class SupplierCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=150)]
    contact_name: Optional[Annotated[str, StringConstraints(max_length=100)]] = None
    email: Optional[EmailStr] = None
    phone: Optional[Annotated[str, StringConstraints(max_length=20)]] = None
    address: Optional[str] = None


# Schema for returning data to client
class ProductOut(SupplierCreate):
    supplier_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
