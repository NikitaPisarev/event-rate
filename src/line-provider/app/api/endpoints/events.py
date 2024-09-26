from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.api.models import EventStatusUpdate
from app.api.schemas.requests import EventCreateRequest
from app.api.schemas.responses import EventIdResponse, EventResponse
from app.core.database import event_collection


router = APIRouter()


@router.post(
    "/events",
    response_description="Create a new event",
    status_code=status.HTTP_201_CREATED
)
async def create_event(event: EventCreateRequest) -> EventIdResponse:
    event_data = event.model_dump(by_alias=True)
    result = await event_collection.insert_one(event_data)
    created_event = await event_collection.find_one({"_id": result.inserted_id})
    return created_event


@router.get(
    "/events",
    response_description="List all events",
    response_model=List[EventIdResponse]
)
async def list_events(length: int = 100) -> list[EventIdResponse]:
    events = await event_collection.find().to_list(length=length)
    return events


@router.get(
    "/events/{event_id}",
    response_description="Get a single event",
    response_model=EventResponse
)
async def get_event(event_id: str) -> EventResponse:
    if (event := await event_collection.find_one({"_id": ObjectId(event_id)})) is not None:
        return event
    raise HTTPException(status_code=404, detail=f"Event {event_id} not found")


@router.patch(
    "/events/{event_id}",
    response_description="Update an event",
    response_model=EventResponse
)
async def update_event_status(event_id: str, status_update: EventStatusUpdate):
    result = await event_collection.update_one({"_id": ObjectId(event_id)}, {"$set": status_update.model_dump()})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    updated_event = await event_collection.find_one({"_id": ObjectId(event_id)})
    return updated_event


@router.delete(
    "/events/{event_id}",
    response_description="Delete an event"
)
async def delete_event(event_id: str) -> JSONResponse:
    delete_result = await event_collection.delete_one({"_id": ObjectId(event_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    return {"message": f"Event {event_id} deleted successfully"}
