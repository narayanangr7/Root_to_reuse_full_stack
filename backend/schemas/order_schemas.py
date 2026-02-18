from pydantic import BaseModel

class OrderCreate(BaseModel):
    user_id: int
    product_id: int

class OrderResponse(BaseModel):
    id: int
    product_states:str
    user_id: int
    product_id: int
    
    class Config:
        from_attributes = True
class OrderUpdate(BaseModel):
    product_states: str
