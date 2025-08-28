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


def build_producer(bootstrap_servers: str) -> KafkaProducer:
    """Build a Kafka producer"""
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: json.dumps(k).encode("utf-8") if k is not None else None,
        linger_ms=10,
        retries=5,
        acks="all"
    )
    return producer