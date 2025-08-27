import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RetrieverConfig:
    "Configuration for the retriever service loaded from environment variables."
    
    # Mongo (Atlas)
    mongodb_uri: str
    mongodb_db_name: str
    mongodb_collection_name: str
    
    # Kafka
    kafka_bootstrap_servers: str
    topic_raw_antisemitic: str
    topic_raw_not_antisemitic: str
    
    # Batch and scheduling
    batch_size: int = 100
    interval_seconds: int = 60
    
    # State handling
    state_file_path: str = "/tmp/retriever_state.json"
    initial_last_processed_iso: Optional[str] = None
    
    @staticmethod
    def from_env() -> "RetrieverConfig":
        return RetrieverConfig(
            mongodb_uri=os.getenv("MONGODB_ATLAS_URI", ""),
            mongodb_db_name=os.getenv("MONGODB_DB_NAME", "IranMalDB"),
            mongodb_collection_name=os.getenv("MONGODB_COLLECTION_NAME", "tweets"),
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            topic_raw_antisemitic=os.getenv("TOPIC_RAW_ANTISEMITIC", "raw_tweets_antisemitic"),
            topic_raw_not_antisemitic=os.getenv("TOPIC_RAW_NOT_ANTISEMITIC", "raw_tweets_not_antisemitic"),
            batch_size=int(os.getenv("RETRIEVER_BATCH_SIZE", "100")),
            interval_seconds=int(os.getenv("RETRIEVER_INTERVAL_SECONDS", "60")),
            state_file_path=os.getenv("RETRIEVER_STATE_PATH", "/tmp/retriever_state.json"),
            initial_last_processed_iso=os.getenv("RETRIEVER_LAST_PROCESSED_ISO"),
        )
    