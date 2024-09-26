from pydantic import BaseModel


class BaseRequest(BaseModel):
    pass


class EventCreateRequest(BaseRequest):
    deadline: str
    status: str
