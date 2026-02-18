from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.camp_models import Camp
from schemas.camp_schemas import CampCreate, CampUpdate, CampResponse
from models.volunteer_models import Volunteer
from models.camp_participant_model import CampParticipant
from utils.email_utils import send_camp_approval_email, send_camp_joined_email

router = APIRouter(prefix="/camp", tags=["Camp"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", response_model=CampResponse)
def create_camp(data: CampCreate, db: Session = Depends(get_db)):
    # Verify the volunteer exists and is approved
    volunteer = db.query(Volunteer).filter(Volunteer.id == data.volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    if volunteer.status != "Approved":
        raise HTTPException(
            status_code=403, 
            detail="Only approved volunteers can propose a camp."
        )

    camp_data = data.model_dump()
    camp = Camp(**camp_data)
    db.add(camp)
    db.commit()
    db.refresh(camp)
    
    # Attach name dynamically for the response
    camp.volunteer_name = volunteer.full_name
    return camp


def format_camp_response(camp):
    # Map the participant objects to the simple schema
    participants_list = []
    if hasattr(camp, 'participants'):
        for p in camp.participants:
            participants_list.append({
                "volunteer_name": p.volunteer.full_name,
                "phone_no": p.volunteer.phone_no
            })
    
    return {
        **camp.__dict__,
        "volunteer_name": camp.volunteer.full_name if camp.volunteer else "Unknown",
        "participants": participants_list
    }

@router.get("/all")
def get_all_camps(db: Session = Depends(get_db)):
    # Publicly show only approved camps with linked volunteer names
    camps = db.query(Camp).filter(Camp.status == "Approved").all()
    return [format_camp_response(c) for c in camps]


@router.get("/requests")
def get_all_camp_requests(db: Session = Depends(get_db)):
    # For admin to see all requests with linked names
    camps = db.query(Camp).all()
    return [format_camp_response(c) for c in camps]


@router.post("/join/{camp_id}")
def join_camp(camp_id: int, username: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Verify user is an approved volunteer
    volunteer = db.query(Volunteer).filter(Volunteer.username == username).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer record not found")
    
    if volunteer.status != "Approved":
        raise HTTPException(status_code=403, detail="Only approved volunteers can join events")

    # 2. Check if camp exists and is approved
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    
    if camp.status != "Approved":
        raise HTTPException(status_code=400, detail="Cannot join a camp that is not yet approved")

    # 3. Check if already joined
    existing = db.query(CampParticipant).filter(
        CampParticipant.camp_id == camp_id,
        CampParticipant.volunteer_id == volunteer.id
    ).first()
    if existing:
        return {"message": "You have already joined this event!"}

    # 4. Join
    participant = CampParticipant(camp_id=camp_id, volunteer_id=volunteer.id)
    db.add(participant)
    db.commit()
    
    # Send Joined Email
    if volunteer.email:
        organizer_name = camp.volunteer.full_name if camp.volunteer else "the admin"
        background_tasks.add_task(send_camp_joined_email, volunteer.email, volunteer.full_name, camp.event_name, organizer_name)
    
    return {"message": "Joined successfully!"}


@router.post("/approve/{camp_id}", response_model=CampResponse)
def approve_camp(camp_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    
    camp.status = "Approved"
    db.commit()
    db.refresh(camp)

    # Send Approval Email to the organizer (camp owner)
    if camp.email:
        background_tasks.add_task(send_camp_approval_email, camp.email, camp.full_name, camp.event_name)

    return camp


@router.get("/{camp_id}", response_model=CampResponse)
def get_camp_by_id(camp_id: int, db: Session = Depends(get_db)):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")
    return camp


@router.get("/volunteer/{volunteer_id}", response_model=list[CampResponse])
def get_camps_by_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    camps = db.query(Camp).filter(Camp.volunteer_id == volunteer_id).all()
    return camps


@router.put("/update/{camp_id}", response_model=CampResponse)
def update_camp(
    camp_id: int,
    data: CampUpdate,
    db: Session = Depends(get_db)
):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(camp, key, value)

    db.commit()
    db.refresh(camp)
    return camp


@router.delete("/delete/{camp_id}")
def delete_camp(camp_id: int, db: Session = Depends(get_db)):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")

    db.delete(camp)
    db.commit()
    return {"message": "Camp removed successfully"}
