import os
from dataclasses import dataclass


@dataclass
class EnricherConfig:
    kafka_bootstrap_servers: str
    group_id: str
    consume_topic_antisemitic: str
    consume_topic_not_antisemitic: str
    produce_topic_antisemitic: str
    produce_topic_not_antisemitic: str

    @staticmethod
    def from_env() -> "EnricherConfig":
        return EnricherConfig(
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092"),
            group_id=os.getenv("ENRICHER_GROUP_ID", "enricher_group"),
            consume_topic_antisemitic=os.getenv(
                "ENRICHER_CONSUME_TOPIC_ANTISEMITIC",
                "preprocessed_tweets_antisemitic"
            ),
            consume_topic_not_antisemitic=os.getenv(
                "ENRICHER_CONSUME_TOPIC_NOT_ANTISEMITIC",
                "preprocessed_tweets_not_antisemitic"
            ),
            produce_topic_antisemitic=os.getenv(
                "ENRICHER_PRODUCE_TOPIC_ANTISEMITIC",
                "enriched_preprocessed_tweets_antisemitic"
            ),
            produce_topic_not_antisemitic=os.getenv(
                "ENRICHER_PRODUCE_TOPIC_NOT_ANTISEMITIC",
                "enriched_preprocessed_tweets_not_antisemitic"
            ),
        )