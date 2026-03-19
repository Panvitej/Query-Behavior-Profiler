# =========================
# DATABASE CONFIGURATION
# =========================

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "query_profiler"
MONGO_COLLECTION = "query_logs"


# PostgreSQL Configuration
POSTGRES_CONFIG = {
    "dbname": "query_profiler",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432
}


# =========================
# APPLICATION SETTINGS
# =========================

# Threshold for slow queries (seconds)
SLOW_QUERY_THRESHOLD = 1.0

# Spike detection multiplier
SPIKE_MULTIPLIER = 2.0

# Number of sample queries to simulate
SIMULATION_ITERATIONS = 20


# =========================
# LOGGING CONFIG
# =========================

LOG_LEVEL = "INFO"


# =========================
# ETL SETTINGS
# =========================

# Batch size for Mongo → PostgreSQL sync
BATCH_SIZE = 100

# Enable / disable SQL sync
ENABLE_SQL_SYNC = True


# =========================
# OPTIONAL (ADVANCED)
# =========================

# TTL for MongoDB logs (seconds) → 7 days
MONGO_TTL_SECONDS = 604800

# Enable anomaly detection (future use)
ENABLE_ANOMALY_DETECTION = False
