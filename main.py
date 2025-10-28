from fastapi import FastAPI
from db.database import engine
from db import models
from api.auth import router as auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventPlanner API - Phase 0")
app.include_router(auth_router)
@app.get("/event")
def eventplanner():
    return {"Welcome to EventPlanner API"}
