from sqlalchemy import Column,String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_states = Column(String, nullable=False ,default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("product.id"))

    user = relationship("User")
    product = relationship("Product")
