from typing import Dict, Any

from .sentiment import SentimentAnalyzer
from .timestamp_extractor import TimestampExtractor
from .weapons import WeaponsExtractor


class DataEnricher:
    def __init__(self):
        self._sentiment_analyzer = SentimentAnalyzer()
        self._weapons_extractor = WeaponsExtractor()
        self._timestamp_extractor = TimestampExtractor()

    def enrich_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        enriched_data = data.copy()
        text = enriched_data['original_text']
        enriched_data['sentiment'] = self._sentiment_analyzer.sentiment_analyzer(text)
        enriched_data['weapons_detected'] = self._weapons_extractor.extract_weapons(text)
        enriched_data['relevant_timestamp'] = self._timestamp_extractor.extract_latest_timestamp(text)
        return enriched_data