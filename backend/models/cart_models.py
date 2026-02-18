from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("product.id"))

    user = relationship("User")
    product = relationship("Product")

    
