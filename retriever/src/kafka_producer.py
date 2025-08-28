from typing import Any, Dict
import json
import logging
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

class Producer:
    def __init__(self, bootstrap_servers: str):
        """Initialize the Kafka producer."""
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
            key_serializer=lambda k: json.dumps(k, default=str).encode("utf-8") if k is not None else None,
            linger_ms=10,
            retries=5,
            acks="all",
        )
        
    def send(self, topic: str, value: Dict[str, Any], key: Any = None) -> None:
        "Send a message to a Kafka topic."
        logger.debug("Producing message", extra={"topic": topic})
        self._producer.send(topic, value=value, key=key)
        
    def flush(self) -> None:
        self._producer.flush()
        
    def close(self) -> None:
        try:
            self._producer.flush()
        finally:
            self._producer.close()
