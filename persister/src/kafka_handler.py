import json
from typing import Iterable

from kafka import KafkaConsumer, KafkaProducer


def build_consumer(bootstrap_servers: str, group_id: str, topics: Iterable[str]) -> KafkaConsumer:
    """Build a Kafka consumer"""
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda v: json.loads(v.decode("utf-8")) if v is not None else None,
        max_poll_records=200,
    )
    return consumer