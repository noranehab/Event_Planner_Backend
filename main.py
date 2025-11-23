from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db import models
from api.auth import router as auth_router
from api.events import router as events_router

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventPlanner API - Phase 0")

# CORS Configuration - MUST BE BEFORE ROUTES
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
#    allow_credentials=True,
#   allow_methods=["*"],
#    allow_headers=["*"],
#)

# Include routers
app.include_router(auth_router)

app.include_router(events_router)

@app.get("/")
def root():
    return {"message": "EventPlanner API is running"}

@app.get("/event")
def eventplanner():
    return {"message": "Welcome to EventPlanner API"}