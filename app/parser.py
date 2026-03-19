import re
import hashlib

class QueryParser:

    @staticmethod
    def normalize(query):
        query = query.lower()
        query = re.sub(r'\d+', '?', query)
        query = re.sub(r"'[^']*'", '?', query)
        query = re.sub(r'\s+', ' ', query)
        return query.strip()

    @staticmethod
    def fingerprint(query):
        return hashlib.md5(query.encode()).hexdigest()

    @staticmethod
    def extract_features(query):
        q = query.lower()
        return {
            "joins": q.count("join"),
            "filters": q.count("where"),
            "group_by": q.count("group by"),
            "order_by": q.count("order by"),
        }
