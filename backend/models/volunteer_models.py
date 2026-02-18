from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Volunteer(Base):
    __tablename__ = "volunteer"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)

    # Use username as the primary link
    username = Column(
        String, 
        ForeignKey("users.username", ondelete="CASCADE"), 
        nullable=False
    )
    # user_phone is stored for reference as per user request
    user_phone = Column(
        String, 
        ForeignKey("users.phone_no", ondelete="CASCADE"), 
        nullable=False
    )

    email = Column(String, nullable=False)
    phone_no = Column(String, nullable=False)
    skills = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default="Pending", nullable=False)

    # Explicitly link via username to avoid join ambiguity
    user = relationship("User", foreign_keys=[username]) 
   

