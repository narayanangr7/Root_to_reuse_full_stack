from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Camp(Base):
    __tablename__ = "camp"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    volunteer_id = Column(Integer, ForeignKey("volunteer.id"), nullable=False)

    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    hours = Column(Integer, nullable=False)
    event_date = Column(String, nullable=False) # Store as YYYY-MM-DD string for simplicity
    message = Column(Text, nullable=True)
    status = Column(String, default="Pending", nullable=False) # For admin approval

    volunteer = relationship("Volunteer")
    participants = relationship("CampParticipant", back_populates="camp", cascade="all, delete-orphan")


 