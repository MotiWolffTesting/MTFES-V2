from .kafka_handler import build_consumer
from .config import PersisterConfig
from .mongo_handler import MongoHandler


def main() -> None:
    config = PersisterConfig.from_env()
    consumer = build_consumer(
        config.kafka_bootstrap_servers,
        config.group_id,
        [config.topic_antisemitic, config.topic_not_antisemitic]
    )
    mongo_handler = MongoHandler(
        config.mongodb_uri, config.mongodb_db_name
    )

    for message in consumer:
        collection = (
            config.mongodb_collection_antisemitic_name
            if message.topic == config.topic_antisemitic
            else config.mongodb_collection_not_antisemitic_name
        )
        document = message.value
        mongo_handler.insert_one(collection, document)
    mongo_handler.close()

if __name__ == "__main__":
    main()