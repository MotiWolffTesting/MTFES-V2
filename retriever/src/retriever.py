import json
import logging
import os
from datetime import datetime
from typing import Any, List, Dict, Optional, Tuple
from dateutil import parser as date_parser
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from .config import RetrieverConfig
from .kafka_producer import Producer

logger = logging.getLogger(__name__)

def _parse_datetime(value: Any) -> Optional[datetime]:
    "Parses a datetime string into a datetime object"
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except Exception:
        return None
    
class MongoRetriever:
    def __init__(self, config: RetrieverConfig, producer: Producer):
        """Initialize the MongoRetriever."""
        self.config = config
        self.producer = producer
        self._client = MongoClient(config.mongodb_uri)
        self._collection: Collection = (
            self._client[config.mongodb_db_name][config.mongodb_collection_name]
        )

        # Load last processed timestamp from state file if exists
        self._last_processed: Optional[str] = self._load_state()
        if not self._last_processed and self.config.initial_last_processed_iso:
            self._last_processed = self.config.initial_last_processed_iso
            
    def _load_state(self) -> Optional[str]:
        "Load the last processed timestamp from the state file."
        path = self.config.state_file_path
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding='utf-8') as f:
                data = json.load(f)
            return data.get("last_processed_iso")
        except Exception:
            return None
        
    def _save_state(self, last_processed_iso: str) -> None:
        "Save the last processed timestamp to the state file."
        try:
            with open(self.config.state_file_path, "w", encoding="utf-8") as f:
                json.dump({"last_processed_iso": last_processed_iso}, f)
        except Exception as e:
            logger.warning("Failed saving state.", extra={"error": str(e)})
            
    def _build_query(self) -> Dict[str, Any]:
        "Build the query to retrieve documents from the database."
        if self._last_processed:
            last_dt = _parse_datetime(self._last_processed)
            if last_dt:
                return {"creatdate": {"$gt": last_dt}}
        return {}
    
    def _is_antisemitic(self, doc: Dict[str, Any]) -> bool:
        "Check if a document is antisemitic."
        for key in ("antisemietic", "antisemitic", "is_antisemitic", "classification"):
            if key in doc:
                val = doc[key]
                if isinstance(val, (int, float)):
                    return int(val) == 0
                if isinstance(val, str):
                    return val.lower() in {"0", "false", "antisemitic", "yes"}
                if isinstance(val, bool):
                    return bool(val)
        return False
    
    def _extract_createdate(self, doc: Dict[str, Any]) -> Optional[datetime]:
        "Extract the createdate from a document"
        for key in ("createdate", "created_at", "createdAt", "created", "date", "timestamp", "time"):
            if key in doc and doc[key]:
                val = doc[key]
                if isinstance(val, datetime):
                    return val
                try:
                    return date_parser.parse(str(val))
                except Exception:
                    pass
        oid = doc.get("_id")
        if isinstance(oid, ObjectId):
            return oid.generation_time
        return None
        
    def _map_record(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        "Map a document to a record."
        text = doc.get("text") or doc.get("original_text") or ""
        cdt = self._extract_createdate(doc)
        mapped = {
            "id": str(doc.get("_id")) if isinstance(doc.get("_id"), ObjectId) else str(doc.get("_id")),
            "createdate": cdt,
            "antisemietic": 1 if self._is_antisemitic(doc) else 0,
            "original_text": text,
        }
        return mapped
    
    def _split_by_class(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        "Split records into antisemitic and non-antisemitic lists."
        antis: List[Dict[str, Any]] = []
        non_antis: List[Dict[str, Any]] = []
        for record in records:
            if record.get("antisemitic", 0) == 1:
                antis.append(record)
            else:
                non_antis.append(record)
        return antis, non_antis
    
    def run_once(self) -> int:
        "Run the retriever once."
        query = self._build_query()
        cursor = (
            self._collection.find(query).sort("creatdate", 1).limit(self.config.batch_size)
        )
        docs = list(cursor)
        if not docs:
            logger.info("No documents found")
            return 0
        
        records = [self._map_record(d) for d in docs]
        antis, non_antis = self._split_by_class(records)
        
        for record in antis:
            self.producer.send(self.config.topic_raw_antisemitic, record, key=record["id"])
        for record in non_antis:
            self.producer.send(self.config.topic_raw_not_antisemitic, record, key=record["id"])
            
        self.producer.flush()
        
        # Update last processed to the latest createdate in this batch
        last_dt = docs[-1].get("createdate")
        if isinstance(last_dt, datetime):
            iso_value = last_dt.isoformat()
        else:
            iso_value = str(last_dt)
        if iso_value:
            self._last_processed = iso_value
            self._save_state(iso_value)
            
        logger.info(
            "Batch published",
            extra={"total": len(records),  "antis": len(antis), "non_antis": len(non_antis)}
        )
        return len(records)

    
    
