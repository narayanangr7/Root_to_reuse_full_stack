from pydantic import BaseModel

class CartCreate(BaseModel):
    quantity:int
    user_id: int
    product_id: int

class CartUpdate(BaseModel):
    quantity: int