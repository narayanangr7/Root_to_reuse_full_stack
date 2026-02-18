from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class CampParticipant(Base):
    __tablename__ = "camp_participants"

    id = Column(Integer, primary_key=True, index=True)
    camp_id = Column(Integer, ForeignKey("camp.id", ondelete="CASCADE"), nullable=False)
    volunteer_id = Column(Integer, ForeignKey("volunteer.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    camp = relationship("Camp", back_populates="participants")
    volunteer = relationship("Volunteer")
