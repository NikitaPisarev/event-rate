from datetime import datetime, timezone
from aiokafka import AIOKafkaProducer
from dateutil import parser
import json
import httpx

from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, LINE_PROVIDER_URL


async def fetch_event(event_id: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LINE_PROVIDER_URL}/events/{event_id}")
        if response.status_code == 200:
            return response.json()
        return None


async def is_event_within_deadline(event_id: str) -> bool:
    event = await fetch_event(event_id)
    if event:
        deadline = event.get('deadline')
        try:
            deadline = parser.parse(deadline)
        except (ValueError, TypeError):
            return False

        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)

        return datetime.now(tz=timezone.utc) < deadline
    return False


async def send_score_to_kafka(event_id: str, new_score: str) -> None:
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        message = {
            'event_id': event_id,
            'score': new_score
        }
        await producer.send_and_wait(KAFKA_TOPIC, json.dumps(message).encode('utf-8'))
    finally:
        await producer.stop()
