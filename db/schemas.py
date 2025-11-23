from pydantic import BaseModel, EmailStr
from datetime import date, time


class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EventCreate(BaseModel):
    title: str
    date: date
    time: time
    location: str
    description: str


class EventResponse(BaseModel):
    id: int
    title: str
    date: date
    time: time
    location: str
    description: str
    organizer_id: int

    class Config:
        orm_mode = True