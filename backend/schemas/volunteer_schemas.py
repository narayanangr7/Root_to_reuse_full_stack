from pydantic import BaseModel

class VolunteerBase(BaseModel):
    full_name: str
    username: str
    user_phone: str
    email: str
    phone_no: str
    skills: str | None = None
    age: int
    location: str
    status: str = "Pending"


class VolunteerCreate(VolunteerBase):
    pass


class VolunteerUpdate(BaseModel):
    full_name: str | None = None
    phone_no: str | None = None
    skills: str | None = None
    age: int | None = None
    location: str | None = None
    status: str | None = None # Added


class VolunteerResponse(VolunteerBase):
    id: int

    class Config:
        from_attributes = True
