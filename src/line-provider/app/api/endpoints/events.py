from datetime import datetime, timezone
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.api.models import Event, EventStatusUpdate
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
    event_data = Event(**event.model_dump()).to_internal()
    result = await event_collection.insert_one(event_data)
    created_event = await event_collection.find_one({"_id": result.inserted_id})
    return created_event


@router.get(
    "/new-events",
    response_description="List all available events"
)
async def get_new_events() -> list[EventResponse]:
    current_time = datetime.now(tz=timezone.utc)

    events_cursor = event_collection.find({"deadline": {"$gt": current_time}})

    events = []
    async for event in events_cursor:
        events.append(EventResponse(
            event_id=str(event.get("_id")),
            deadline=event.get("deadline"),
            status=event.get("status")
        ))

    if not events:
        raise HTTPException(status_code=404, detail="No available events found.")

    return events


@router.get(
    "/events",
    response_description="List all events",
)
async def list_events(length: int = 100) -> list[EventIdResponse]:
    events = await event_collection.find().to_list(length=length)
    return events


@router.get(
    "/events/{event_id}",
    response_description="Get a single event",
)
async def get_event(event_id: str) -> EventResponse:
    if (event := await event_collection.find_one({"_id": ObjectId(event_id)})) is not None:
        return event
    raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")


@router.patch(
    "/events/{event_id}",
    response_description="Update an event",
    response_model=EventResponse
)
async def update_event_status(event_id: str, status_update: EventStatusUpdate):
    result = await event_collection.update_one({"_id": ObjectId(event_id)}, {"$set": status_update.model_dump()})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")

    updated_event = await event_collection.find_one({"_id": ObjectId(event_id)})
    return updated_event


@router.delete(
    "/events/{event_id}",
    response_description="Delete an event"
)
async def delete_event(event_id: str) -> JSONResponse:
    delete_result = await event_collection.delete_one({"_id": ObjectId(event_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found.")

    return {"message": f"Event {event_id} deleted successfully."}
