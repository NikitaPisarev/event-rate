from pydantic import BaseModel, Field
from bson import ObjectId


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    deadline: str = Field(...)
    status: str = Field(...)

    model_config = {
        "title": "Event",
        "description": "A model representing an event in the system",
        "schema": {
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "Unique identifier for the event (MongoDB _id)"
                },
                "deadline": {
                    "type": "string",
                    "format": "date-time",
                    "description": "The deadline for submitting scores for the event"
                },
                "status": {
                    "type": "string",
                    "description": "Current status of the event"
                }
            },
            "required": ["event_id", "deadline", "status"]
        }
    }


class EventStatusUpdate(BaseModel):
    status: str = Field(...)

    model_config = {
        "title": "EventStatusUpdate",
        "description": "A model for updating the status of an event",
        "schema": {
            "properties": {
                "status": {
                    "type": "string",
                    "description": "New status of the event"
                }
            },
            "required": ["status"]
        }
    }
