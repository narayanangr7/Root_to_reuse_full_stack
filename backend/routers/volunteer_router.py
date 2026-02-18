from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.volunteer_models import Volunteer
from schemas.volunteer_schemas import VolunteerBase,VolunteerCreate,VolunteerResponse,VolunteerUpdate
from utils.email_utils import send_volunteer_approval_email

router = APIRouter(prefix="/volunteers", tags=["Volunteers"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=VolunteerResponse)
def create_volunteer(data: VolunteerCreate, db: Session = Depends(get_db)):
    volunteer = Volunteer(**data.model_dump())
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer


@router.get("", response_model=list[VolunteerResponse])
def get_all_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).all()


@router.get("/user/{username}", response_model=VolunteerResponse)
def get_volunteer_by_username(username: str, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.username == username).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer record not found")
    return volunteer


@router.get("/{volunteer_id}", response_model=VolunteerResponse)
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer


@router.put("/{volunteer_id}", response_model=VolunteerResponse)
def update_volunteer(
    volunteer_id: int,
    data: VolunteerUpdate,
    db: Session = Depends(get_db)
):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(volunteer, key, value)

    db.commit()
    db.refresh(volunteer)
    return volunteer


@router.post("/{volunteer_id}/approve", response_model=VolunteerResponse)
def approve_volunteer(volunteer_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    volunteer.status = "Approved"
    db.commit()
    db.refresh(volunteer)

    # Send Approval Email
    if volunteer.email:
        print(f"[DEBUG] Queueing approval email for {volunteer.email}")
        background_tasks.add_task(send_volunteer_approval_email, volunteer.email, volunteer.full_name)
    else:
        print("[DEBUG] No email found for volunteer, skipping notification.")

    return volunteer


@router.delete("/{volunteer_id}")
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")

    db.delete(volunteer)
    db.commit()
    return {"message": "Volunteer removed successfully"}
