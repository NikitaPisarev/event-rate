import json
import logging
from aiokafka import AIOKafkaConsumer
from bson import ObjectId

from app.config import get_settings
from app.core.database import event_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


async def consume_scores() -> None:
    consumer = AIOKafkaConsumer(
        settings.kafka_broker.topic[0],
        bootstrap_servers=settings.kafka_broker.bootstrap_servers,
        group_id="line-provider-group",
    )
    await consumer.start()
    try:
        async for message in consumer:
            event_data = message.value.decode('utf-8')
            logger.info(f"Message received from Kafka: {event_data}")

            await procces_event_message(event_data)
    finally:
        await consumer.stop()


async def procces_event_message(event_data: str) -> None:
    data = json.loads(event_data)
    event_id = data.get('event_id')
    new_score = data.get('score')

    status = "Highly rated" if new_score >= 3 else "Lowly rated"

    result = await event_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"status": status}}
    )

    if result.matched_count > 0:
        logger.info(f"Event {event_id} updated successfully. Status: {status}")
    else:
        logger.error(f"Event {event_id} not found")
