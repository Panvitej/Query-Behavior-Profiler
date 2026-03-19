import psycopg2
from collections import defaultdict
from app.parser import QueryParser
from config.settings import POSTGRES_CONFIG

class SQLSync:

    def __init__(self, mongo_db):
        self.mongo = mongo_db
        self.pg = psycopg2.connect(**POSTGRES_CONFIG)

    def aggregate(self):
        data = self.mongo.fetch_all()
        grouped = defaultdict(list)

        for d in data:
            grouped[d["normalized_query"]].append(d)

        results = []

        for norm, docs in grouped.items():
            times = [x["execution_time"] for x in docs]
            rows = [x["rows_returned"] for x in docs]

            results.append({
                "hash": QueryParser.fingerprint(norm),
                "norm": norm,
                "avg": sum(times)/len(times),
                "max": max(times),
                "min": min(times),
                "count": len(times),
                "rows": sum(rows),
                "first": docs[0]["created_at"],
                "last": docs[-1]["created_at"]
            })

        return results

    def sync(self):
        cursor = self.pg.cursor()
        data = self.aggregate()

        for r in data:
            cursor.execute("""
            INSERT INTO query_metrics (
                query_hash, normalized_query,
                avg_execution_time, max_execution_time, min_execution_time,
                execution_count, total_rows,
                first_seen, last_seen
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (query_hash)
            DO UPDATE SET
                avg_execution_time = EXCLUDED.avg_execution_time,
                execution_count = query_metrics.execution_count + EXCLUDED.execution_count,
                total_rows = query_metrics.total_rows + EXCLUDED.total_rows,
                last_seen = EXCLUDED.last_seen;
            """, (
                r["hash"], r["norm"], r["avg"], r["max"], r["min"],
                r["count"], r["rows"], r["first"], r["last"]
            ))

        self.pg.commit()
