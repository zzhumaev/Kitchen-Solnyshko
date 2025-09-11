from pydantic import BaseModel
from typing import Optional, List, Literal

class UnitCreate(BaseModel):
    name: str
    short: str

class UnitRead(UnitCreate):
    id: int
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    unit_id: int
    sku: Optional[str] = None

class ProductRead(ProductCreate):
    id: int
    class Config:
        from_attributes = True

class LocationCreate(BaseModel):
    name: str

class LocationRead(LocationCreate):
    id: int
    class Config:
        from_attributes = True

class StockRead(BaseModel):
    product_id: int
    location_id: int
    qty: float

class DocItemIn(BaseModel):
    product_id: int
    location_id: int
    qty: float

class DocumentCreate(BaseModel):
    type: Literal["in","out","invent"]
    created_by: Optional[str] = None
    items: List[DocItemIn]

class DocumentRead(BaseModel):
    id: int
    type: str
    class Config:
        from_attributes = True
