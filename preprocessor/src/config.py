import os
from dataclasses import dataclass
from typing import List

@dataclass
class PreprocessorConfig:
    kafka_bootstrap_servers: str
    group_id: str
    consume_topics: List[str]
    produce_topic_antisemitic: str
    produce_topic_not_antisemitic: str
    
    # Text processing
    language: str = "english"
    
    @staticmethod
    def from_env() -> "PreprocessorConfig":
        topics_raw = os.getenv(
            "PREPROCESSOR_CONSUME_TOPICS",
            "raw_tweets_antisemitic,raw_tweets_not_antisemitic",
        )
        return PreprocessorConfig(
            kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            group_id=os.getenv("PREPROCESSOR_GROUP_ID", "preprocessor-group"),
            consume_topics=[t.strip() for t in topics_raw.split(",") if t.strip()], # list of topics to consume from
            produce_topic_antisemitic=os.getenv(
                "TOPIC_PREPROCESSED_ANTISEMITIC", "preprocessed_tweets_antisemitic"
            ),
            produce_topic_not_antisemitic=os.getenv(
                "TOPIC_PREPROCESSED_NOT_ANTISEMITIC", "preprocessed_tweets_not_antisemitic"
            ),
            language=os.getenv("PREPROCESSOR_LANGUAGE", "english"),
        )
    
    
    