from functools import lru_cache
from pathlib import Path
from pydantic import AnyHttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent


class MongoDatabase(BaseModel):
    MONGO_USER: str = "mongo"
    MONGO_HOST: str = "mongo"
    MONGO_PASSWORD: str = "123"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "event_store"


class Security(BaseModel):
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    backend_cors_origins: list[AnyHttpUrl] = []


class KafkaBroker(BaseModel):
    topic: str = "scores"
    bootstrap_servers: str = "kafka:9092"


class Settings(BaseSettings):
    security: Security
    database: MongoDatabase
    kafka_broker: KafkaBroker

    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="_",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
