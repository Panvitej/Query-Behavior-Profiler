import pandas as pd
from app.core import Database, QueryLogger

class QueryAnalyzer:
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def slow_queries(self, threshold=1.0):
        return self.df[self.df["execution_time"] > threshold]

    def frequent_queries(self):
        return self.df["normalized_query"].value_counts()

    def spikes(self):
        mean = self.df["execution_time"].mean()
        return self.df[self.df["execution_time"] > mean * 2]

    def stats(self):
        return self.df.groupby("normalized_query")["execution_time"].agg(
            ["mean", "max", "count"]
        )


class Optimizer:
    @staticmethod
    def suggest(query):
        q = query.lower()
        suggestions = []

        if "select *" in q:
            suggestions.append("Avoid SELECT *")

        if "where" in q:
            suggestions.append("Consider indexing WHERE columns")

        if "join" in q:
            suggestions.append("Ensure JOIN columns are indexed")

        if "order by" in q:
            suggestions.append("Optimize ORDER BY usage")

        return suggestions


class ProfilerEngine:
    def __init__(self):
        self.db = Database()
        self.logger = QueryLogger(self.db)

    def simulate_data(self):
        queries = [
            "SELECT * FROM users WHERE id = 1",
            "SELECT name FROM users WHERE age > 30",
            "SELECT * FROM orders JOIN users ON users.id = orders.user_id",
        ]

        for _ in range(20):
            for q in queries:
                exec_time = (abs(hash(q)) % 100) / 50.0
                rows = abs(hash(q)) % 100
                self.logger.log(q, exec_time, rows)

    def run(self):
        data = self.db.fetch_all()

        if not data:
            print("No data found.")
            return

        analyzer = QueryAnalyzer(data)

        print("\n=== Slow Queries ===")
        print(analyzer.slow_queries())

        print("\n=== Frequent Queries ===")
        print(analyzer.frequent_queries())

        print("\n=== Spikes ===")
        print(analyzer.spikes())

        print("\n=== Stats ===")
        print(analyzer.stats())

        print("\n=== Optimization Suggestions ===")
        for q in analyzer.df["query_text"].head(5):
            print(q, "->", Optimizer.suggest(q))
