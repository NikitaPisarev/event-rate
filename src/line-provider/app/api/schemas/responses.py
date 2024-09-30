from datetime import datetime
from pydantic import BaseModel, model_validator

from app.api.models import EventStatus


class BaseResponse(BaseModel):
    pass


class EventIdResponse(BaseResponse):
    event_id: str

    @model_validator(mode="before")
    def convert_mongo_id(cls, values):
        if "_id" in values:
            values["event_id"] = str(values.pop("_id"))
        return values


class EventResponse(EventIdResponse):
    deadline: datetime
    status: EventStatus
