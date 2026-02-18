# schemas/product_schema.py
from pydantic import BaseModel
from typing import Optional
class ProductCreate(BaseModel):
    
    category_id:int
    name: str
    price: int
    description: str
    product_type: str 
    material: str 
    length: str 
    weight: str 
    shelf_life: str 
    usage: str 
    image: Optional[str] = None

class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True    # Pydantic v2 ORM mode


class ProductUpdate(BaseModel):
    
    category_id:Optional[int] = None
    name:  Optional[str] = None
    price: Optional[int] = None
    description:Optional[str] = None
    product_type: Optional[str] = None
    material: Optional[str] = None
    length: Optional[str]= None 
    weight: Optional[str] = None
    shelf_life: Optional[str] = None
    usage: Optional[str] = None