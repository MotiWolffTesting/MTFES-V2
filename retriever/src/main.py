import logging 
import signal
import sys
import time
from .config import RetrieverConfig
from .kafka_producer import Producer
from .retriever import MongoRetriever

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

def main() -> None:
    "Main function to handle retriever"
    config = RetrieverConfig.from_env()
    producer = Producer(config.kafka_bootstrap_servers)
    retriever = MongoRetriever(config, producer)
    
    running = True
    
    def handle_sigterm(sigterm, frame):
        "Handle a signal termination."
        nonlocal running
        running = False
        
    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    while running:
        try:
            retriever.run_once()
        except Exception as e:
            logging.exception(f"Retriever failed: {e}")
        time.sleep(config.interval_seconds) 
        
    producer.close()
    
if __name__ == "__main__":
    main()