import logging
import signal
import time
# Import configuration, preprocessor logic, and Kafka helpers
from .config import PreprocessorConfig
from .preprocessor import TextPreprocessor, transform_message
from .kafka_handler import build_consumner, build_producer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

def main() -> None:
    "Main function for Text PreProcessor"
    # Load configuration from environment variables
    config = PreprocessorConfig.from_env()
    # Create Kafka consumer and producer
    consumer = build_consumner(
        config.kafka_bootstrap_servers, config.group_id, config.consume_topics
    )
    producer = build_producer(config.kafka_bootstrap_servers)
    # Initialize text preprocessor
    pre = TextPreprocessor(language=config.language)
    
    running = True
    
    def handle_sigterm(sigterm, frame):
        # Graceful shutdown on SIGINT/SIGTERM
        nonlocal running
        running = False
        
    signal.signal(signal.SIGINT, handler=handle_sigterm)
    signal.signal(signal.SIGTERM, handler=handle_sigterm)
    
    while running:
        try:
            # Poll for new Kafka messages
            for message in consumer.poll(timeout_ms=1000).values():
                for record in message:
                    value = record.value
                    # Transform message using preprocessor
                    transformed = transform_message(value, pre)
                    # Route based on antisemitic flag (supports both 'antisemitic' and legacy 'antisemietic')
                    flag = transformed.get("antisemitic")
                    if flag is None:
                        flag = transformed.get("antisemietic", 0)
                    topic = (
                        config.produce_topic_antisemitic if int(flag or 0) == 1
                        else config.produce_topic_not_antisemitic
                    )
                    # Send transformed message to Kafka
                    producer.send(topic, transformed, key=transformed.get("id"))
            producer.flush()
        except Exception as e:
            # Log errors and wait before retrying
            logging.exception(f"Preprocessor failed: {e}")
            time.sleep(1)
            
if __name__ == "__main__":
    main()