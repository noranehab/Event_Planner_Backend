from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import get_db
from api.utils import get_current_user

router = APIRouter(prefix="/events", tags=["Events"])


# -------------------------------------------------
# CREATE EVENT (Organizer only)
# -------------------------------------------------
@router.post("/create", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_event = models.Event(
        title=event.title,
        date=event.date,
        time=event.time,
        location=event.location,
        description=event.description,
        organizer_id=user.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # Mark creator as ORGANIZER
    organizer_entry = models.EventAttendee(
        user_id=user.id,
        event_id=new_event.id,
        role="organizer"
    )
    db.add(organizer_entry)
    db.commit()

    return new_event


# -------------------------------------------------
# VIEW EVENTS USER ORGANIZES
# -------------------------------------------------
@router.get("/organized", response_model=list[schemas.EventResponse])
def get_my_events(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    events = db.query(models.Event).filter(
        models.Event.organizer_id == user.id
    ).all()
    return events


# -------------------------------------------------
# VIEW EVENTS USER IS INVITED TO
# -------------------------------------------------
@router.get("/invited", response_model=list[schemas.EventResponse])
def get_invited_events(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    records = db.query(models.EventAttendee).filter(
        models.EventAttendee.user_id == user.id,
        models.EventAttendee.role == "attendee"
    ).all()

    return [record.event for record in records]


# -------------------------------------------------
# INVITE USER TO EVENT
# -------------------------------------------------
@router.post("/{event_id}/invite/{user_id}")
def invite_user(
    event_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = db.query(models.Event).filter(
        models.Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only organizer can invite users")

    invitation = models.EventAttendee(
        user_id=user_id,
        event_id=event_id,
        role="attendee"
    )

    db.add(invitation)
    db.commit()

    return {"message": "User invited successfully"}


# -------------------------------------------------
# DELETE EVENT (Organizer only)
# -------------------------------------------------
@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    event = db.query(models.Event).filter(
        models.Event.id == event_id
    ).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer_id != user.id:
        raise HTTPException(status_code=403, detail="Only organizer can delete event")

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}


# -------------------------------------------------
# UPDATE ATTENDANCE (Going / Maybe / Not Going)
# -------------------------------------------------
@router.post("/{event_id}/attendance")
def update_attendance(
    event_id: int,
    data: schemas.AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    attendee = db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id,
        models.EventAttendee.user_id == current_user.id
    ).first()

    if not attendee:
        raise HTTPException(status_code=404, detail="You are not invited to this event")

    attendee.status = data.status
    db.commit()

    return {"message": "Attendance updated", "status": data.status}


# -------------------------------------------------
# ORGANIZER VIEW ATTENDEES & STATUS
# -------------------------------------------------
@router.get("/{event_id}/attendees")
def list_attendees(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    organizer_entry = db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id,
        models.EventAttendee.user_id == current_user.id,
        models.EventAttendee.role == "organizer"
    ).first()

    if not organizer_entry:
        raise HTTPException(status_code=403, detail="Only organizers can view attendees")

    attendees = db.query(models.EventAttendee).filter(
        models.EventAttendee.event_id == event_id
    ).all()

    return [
        {
            "user_id": a.user_id,
            "role": a.role,
            "status": a.status
        }
        for a in attendees
    ]


# -------------------------------------------------
# SEARCH EVENTS
# -------------------------------------------------
@router.get("/search")
def search_events(
    keyword: str = "",
    start_date: str | None = None,
    end_date: str | None = None,
    role: str | None = None,   # organizer / attendee
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Event)

    if keyword:
        query = query.filter(
            models.Event.title.ilike(f"%{keyword}%") |
            models.Event.description.ilike(f"%{keyword}%")
        )

    if start_date:
        query = query.filter(models.Event.date >= start_date)

    if end_date:
        query = query.filter(models.Event.date <= end_date)

    if role in ["organizer", "attendee"]:
        query = query.join(models.EventAttendee).filter(
            models.EventAttendee.user_id == current_user.id,
            models.EventAttendee.role == role
        )

    return query.all()
