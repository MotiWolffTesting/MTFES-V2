import os
from dataclasses import dataclass


@dataclass
class PersisterConfig:
    mongodb_uri: str
    mongodb_db_name: str
    mongodb_collection_antisemitic_name: str
    mongodb_collection_not_antisemitic_name: str

    kafka_bootstrap_servers: str
    group_id: str
    topic_antisemitic: str
    topic_not_antisemitic: str

    @staticmethod
    def from_env() -> "PersisterConfig":
        return PersisterConfig(
            mongodb_uri=os.getenv("MONGODB_URI", "localhost:27017"),
            mongodb_db_name=os.getenv("MONGODB_DB_NAME", "PersisterIranMalDB"),
            mongodb_collection_antisemitic_name=os.getenv("MONGODB_COLLECTION_ANTISEMITIC_NAME", "tweets_antisemitic"),
            mongodb_collection_not_antisemitic_name=os.getenv("MONGODB_COLLECTION_NOT_ANTISEMITIC_NAME", "tweets_not_antisemitic"),
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            group_id=os.getenv("PERSISTER_GROUP_ID", "persister_group"),
            topic_antisemitic=os.getenv(
                "TOPIC_ANTISEMITIC",
                "enriched_preprocessed_tweets_antisemitic"
            ),
            topic_not_antisemitic=os.getenv(
                "TOPIC_NOT_ANTISEMITIC",
                "enriched_preprocessed_tweets_not_antisemitic"
            )
        )