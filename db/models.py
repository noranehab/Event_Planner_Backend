from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Relationships
    organized_events = relationship(
        "Event",
        back_populates="organizer",
        cascade="all, delete-orphan"
    )

    event_participation = relationship(
        "EventAttendee",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id"))

    organizer = relationship(
        "User",
        back_populates="organized_events"
    )

    attendees = relationship(
        "EventAttendee",
        back_populates="event",
        cascade="all, delete-orphan"
    )

class EventAttendee(Base):
    __tablename__ = "event_attendees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    role = Column(String, default="attendee")  # "organizer" or "attendee"
    status = Column(String, default=None, nullable=True) # Going / Maybe / Not Going

    event = relationship(
        "Event",
        back_populates="attendees"
    )

    user = relationship(
        "User",
        back_populates="event_participation"
    )