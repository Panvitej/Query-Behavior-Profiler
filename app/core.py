from pymongo import MongoClient
from datetime import datetime
from config.settings import MONGO_URI, MONGO_DB

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        self.collection = self.db["query_logs"]
        self._create_indexes()

    def _create_indexes(self):
        self.collection.create_index("normalized_query")
        self.collection.create_index("execution_time")
        self.collection.create_index("created_at")

    def insert_log(self, query, normalized, exec_time, rows):
        self.collection.insert_one({
            "query_text": query,
            "normalized_query": normalized,
            "execution_time": exec_time,
            "rows_returned": rows,
            "created_at": datetime.utcnow()
        })

    def fetch_all(self):
        return list(self.collection.find())


class QueryLogger:
    def __init__(self, db):
        self.db = db

    def log(self, query, exec_time, rows):
        from app.parser import QueryParser
        normalized = QueryParser.normalize(query)
        self.db.insert_log(query, normalized, exec_time, rows)
