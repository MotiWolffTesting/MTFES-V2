from .config import EnricherConfig
from .enricher import DataEnricher
from .kafka_handler import build_consumer, build_producer


def main() -> None:
    config = EnricherConfig.from_env()
    kafka_consumer = build_consumer(bootstrap_servers=config.kafka_bootstrap_servers, group_id=config.group_id,
                                    topics=[config.consume_topic_antisemitic, config.consume_topic_not_antisemitic])
    kafka_producer = build_producer(
        bootstrap_servers=config.kafka_bootstrap_servers
    )
    data_enricher = DataEnricher()

    for message in kafka_consumer:
        enriched_data = data_enricher.enrich_data(message.value)
        topic = (
            config.produce_topic_antisemitic
            if message.topic == config.consume_topic_antisemitic
            else config.produce_topic_not_antisemitic
        )
        kafka_producer.send(topic, enriched_data)
    kafka_producer.flush()


if __name__ == "__main__":
    main()