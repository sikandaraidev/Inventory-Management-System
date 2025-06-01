from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ProductMetadataSchema(BaseModel):
    product_id: int
    name: str
    tags: List[str] = Field(default_factory=list)
    specifications: Dict[str, str] = Field(default_factory=dict)
    care_instructions: Optional[str] = ""
    seo_title: Optional[str] = ""
    seo_description: Optional[str] = ""
    vendor_notes: Optional[str] = ""

    # @classmethod
    # def from_sql_product(cls, product_obj):
    #     """Converts a SQLAlchemy Product instance to clean Mongo-safe dict"""
    #     return cls(
    #         product_id=product_obj.product_id,
    #         name=product_obj.name,
    #         tags=getattr(product_obj, "tags", []),
    #         specifications=getattr(product_obj, "specifications", {}),
    #         care_instructions=getattr(product_obj, "care_instructions", "") or "",
    #         seo_title=getattr(product_obj, "seo_title", "") or "",
    #         seo_description=getattr(product_obj, "seo_description", "") or "",
    #         vendor_notes=getattr(product_obj, "vendor_notes", "") or "",
    #     )
