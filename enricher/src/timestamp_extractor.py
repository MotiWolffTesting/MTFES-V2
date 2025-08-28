import re
from datetime import date


class TimestampExtractor:
    def __init__(self):
        self._timestamp_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")

    def extract_latest_timestamp(self, text: str) -> str:
        """Find the timestamp in the text"""
        words = text.split()
        last_timestamp = None
        for word in words:
            if re.match(self._timestamp_pattern, word):
                current_timestamp = date.fromisoformat(word)
                if not last_timestamp or current_timestamp > last_timestamp:
                    last_timestamp = current_timestamp
        return last_timestamp.strftime("%d-%m-%Y") if last_timestamp else ""