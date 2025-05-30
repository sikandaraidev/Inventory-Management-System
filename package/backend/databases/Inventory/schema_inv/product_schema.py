from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field
from pydantic.types import StringConstraints


class ProductCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=150)]
    sku: Annotated[str, StringConstraints(min_length=3, max_length=100)]
    category_id: Annotated[int, Field(gt=0)]
    supplier_id: Annotated[int, Field(gt=0)]
    cost_price: Annotated[float, Field(gt=0)]
    selling_price: Annotated[float, Field(gt=0)]
    quantity_in_stock: Annotated[int, Field(ge=0)] = 0
    expiry_date: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
    description: Optional[str] = None
    status: Annotated[str, StringConstraints(pattern="^(active|inactive)$")] = "active"


# Schema for returning data to client
class ProductOut(ProductCreate):
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2
