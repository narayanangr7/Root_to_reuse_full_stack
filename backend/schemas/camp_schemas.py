from pydantic import BaseModel

class CampBase(BaseModel):
    event_name: str
    full_name: str
    volunteer_id: int
    email: str
    phone: str
    address: str
    hours: int
    event_date: str
    message: str | None = None
    status: str = "Pending"


class CampCreate(CampBase):
    pass


class CampUpdate(BaseModel):
    event_name: str | None = None
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    hours: int | None = None
    event_date: str | None = None
    message: str | None = None
    status: str | None = None


class ParticipantOut(BaseModel):
    volunteer_name: str
    phone_no: str

class CampResponse(CampBase):
    id: int
    volunteer_name: str | None = None
    participants: list[ParticipantOut] = []

    class Config:
        from_attributes = True
