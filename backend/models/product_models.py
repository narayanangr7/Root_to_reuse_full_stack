from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category.id"))

    name = Column(String, nullable=False)
    price = Column(Integer)
    description = Column(Text, nullable=False)
    product_type = Column(String)
    material = Column(String)
    length = Column(String)
    weight = Column(String)
    shelf_life = Column(String)
    usage = Column(String)
    image = Column(String, nullable=True)

    category = relationship("Category", back_populates="products")

    