from pydantic import BaseModel

class CategoryBase(BaseModel):

    name:str
    content:str