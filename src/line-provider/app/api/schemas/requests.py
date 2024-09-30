from datetime import datetime
from pydantic import BaseModel, Field
from dateutil import parser

from app.api.models import EventStatus


class BaseRequest(BaseModel):
    pass


class EventCreateRequest(BaseRequest):
    deadline: str = Field(..., format="date-time")
    status: EventStatus

    def parse_deadline(cls, value: str) -> datetime:
        try:
            return parser.parse(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {value}.")

    def to_internal(self):
        return {
            "deadline": self.parse_deadline(self.deadline),
            "status": self.status
        }

    class Config:
        json_schema_extra = {
            "example": {
                "deadline": "30/09/2024 23:59",
                "status": "In Progress"
            }
        }
