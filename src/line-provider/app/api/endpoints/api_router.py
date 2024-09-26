from fastapi import APIRouter

from app.api.endpoints import events

event_router = APIRouter()
event_router.include_router(events.router, tags=["events"])
