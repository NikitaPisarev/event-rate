import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.database import create_indexes
from app.core.kafka_consumer import consume_scores
from app.api.endpoints.api_router import event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    asyncio.create_task(consume_scores())
    yield


app = FastAPI(
    title="event-rate",
    version="1.0.0",
    description="System for receiving user ratings on events",
    openapi_url="/openapi.json",
    docs_url="/",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).rstrip("/")
        for origin in get_settings().security.backend_cors_origins
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router)


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200",
    status_code=status.HTTP_200_OK,
)
async def get_health() -> dict:
    return {"status": "OK"}
