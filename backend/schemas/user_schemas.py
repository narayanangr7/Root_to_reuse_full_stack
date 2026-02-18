from pydantic import BaseModel

class SingUpBase(BaseModel):
    username:str
    password:str
    phone_no:str
    email:str

class loginUser(BaseModel):
    id:int
    username:str
    Password:str