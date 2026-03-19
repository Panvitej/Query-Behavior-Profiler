from app.engine import ProfilerEngine
from app.sync import SQLSync
from app.core import Database

def main():
    engine = ProfilerEngine()
    engine.simulate_data()
    engine.run()

    print("\n=== Syncing to PostgreSQL ===")
    sync = SQLSync(Database())
    sync.sync()

if __name__ == "__main__":
    main()
