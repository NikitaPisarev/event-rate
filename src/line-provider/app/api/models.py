from datetime import datetime
from pydantic import BaseModel, Field
from dateutil import parser
from bson import ObjectId
from enum import Enum


class EventStatus(str, Enum):
    IN_PROGRESS = "In Progress"
    HIGH_SCORE = "Rated High"
    LOW_SCORE = "Rated Low"


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    deadline: str = Field(..., format="date-time")
    status: EventStatus

    def parse_deadline(cls, value: str) -> datetime:
        try:
            return parser.parse(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {value}.")

    def to_internal(self):
        parsed_deadline = self.parse_deadline(self.deadline)
        return {
            "event_id": self.event_id or str(ObjectId()),
            "deadline": parsed_deadline,
            "status": self.status,
        }

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": str(ObjectId()),
                "deadline": "2024-12-31T23:59:59",
                "status": "In Progress",
            }
        }


class EventStatusUpdate(BaseModel):
    status: EventStatus

    class Config:
        json_schema_extra = {"example": {"status": "Rated High"}}
