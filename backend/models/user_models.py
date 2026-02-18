from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone_no = Column(String, nullable=False, unique=True) # Changed from Integer
    email = Column(String, nullable=False)
    

   

