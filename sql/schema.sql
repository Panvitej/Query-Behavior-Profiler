-- ============================================================
-- QUERY PROFILER - ENTERPRISE ANALYTICS SCHEMA
-- ============================================================

-- =========================
-- EXTENSIONS
-- =========================
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- =========================
-- CORE QUERY DIMENSION
-- =========================
CREATE TABLE IF NOT EXISTS queries (
    query_id BIGSERIAL PRIMARY KEY,
    query_hash TEXT UNIQUE NOT NULL,
    normalized_query TEXT NOT NULL,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL
);

-- =========================
-- EXECUTION METRICS (FACT TABLE)
-- =========================
CREATE TABLE IF NOT EXISTS query_executions (
    execution_id BIGSERIAL PRIMARY KEY,
    query_id BIGINT REFERENCES queries(query_id),

    execution_time DOUBLE PRECISION NOT NULL,
    rows_returned BIGINT,
    cpu_time DOUBLE PRECISION,
    memory_usage DOUBLE PRECISION,

    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- AGGREGATED METRICS
-- =========================
CREATE TABLE IF NOT EXISTS query_aggregates (
    query_id BIGINT PRIMARY KEY REFERENCES queries(query_id),

    avg_execution_time DOUBLE PRECISION,
    max_execution_time DOUBLE PRECISION,
    min_execution_time DOUBLE PRECISION,

    execution_count BIGINT,
    total_rows BIGINT,

    p95_execution_time DOUBLE PRECISION,
    p99_execution_time DOUBLE PRECISION,

    last_updated TIMESTAMP
);

-- =========================
-- FEATURE EXTRACTION TABLE
-- =========================
CREATE TABLE IF NOT EXISTS query_features (
    query_id BIGINT PRIMARY KEY REFERENCES queries(query_id),

    join_count INT,
    filter_count INT,
    group_by_count INT,
    order_by_count INT,
    subquery_count INT
);

-- =========================
-- INDEX RECOMMENDATIONS
-- =========================
CREATE TABLE IF NOT EXISTS index_recommendations (
    id BIGSERIAL PRIMARY KEY,
    query_id BIGINT REFERENCES queries(query_id),

    recommended_index TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- ANOMALY DETECTION LOG
-- =========================
CREATE TABLE IF NOT EXISTS query_anomalies (
    id BIGSERIAL PRIMARY KEY,
    query_id BIGINT REFERENCES queries(query_id),

    anomaly_score DOUBLE PRECISION,
    description TEXT,

    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- TIME-SERIES SNAPSHOT TABLE
-- =========================
CREATE TABLE IF NOT EXISTS query_time_series (
    id BIGSERIAL PRIMARY KEY,
    query_id BIGINT REFERENCES queries(query_id),

    execution_time DOUBLE PRECISION,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- INDEXES (PERFORMANCE CRITICAL)
-- =========================

-- Query lookup
CREATE INDEX idx_queries_hash ON queries(query_hash);

-- Execution tracking
CREATE INDEX idx_exec_query_id ON query_executions(query_id);
CREATE INDEX idx_exec_time ON query_executions(execution_time);
CREATE INDEX idx_exec_timestamp ON query_executions(executed_at);

-- Aggregates
CREATE INDEX idx_agg_exec_time ON query_aggregates(avg_execution_time);
CREATE INDEX idx_agg_count ON query_aggregates(execution_count);

-- Time-series
CREATE INDEX idx_timeseries_query_time 
ON query_time_series(query_id, recorded_at DESC);

-- =========================
-- MATERIALIZED VIEWS (FAST ANALYTICS)
-- =========================

-- Slow queries
CREATE MATERIALIZED VIEW slow_queries AS
SELECT q.query_hash, a.avg_execution_time, a.execution_count
FROM query_aggregates a
JOIN queries q ON q.query_id = a.query_id
WHERE a.avg_execution_time > 1.0;

-- Frequently executed queries
CREATE MATERIALIZED VIEW frequent_queries AS
SELECT q.query_hash, a.execution_count
FROM query_aggregates a
JOIN queries q ON q.query_id = a.query_id
ORDER BY a.execution_count DESC;

-- =========================
-- ADVANCED ANALYTICS VIEW
-- =========================

CREATE VIEW query_performance_summary AS
SELECT 
    q.query_hash,
    a.execution_count,
    a.avg_execution_time,
    a.p95_execution_time,
    a.p99_execution_time,
    f.join_count,
    f.filter_count
FROM queries q
JOIN query_aggregates a ON q.query_id = a.query_id
LEFT JOIN query_features f ON q.query_id = f.query_id;

-- =========================
-- TRIGGERS (AUTO UPDATE AGGREGATES)
-- =========================

CREATE OR REPLACE FUNCTION update_query_aggregates()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO query_aggregates (query_id, avg_execution_time, max_execution_time, min_execution_time, execution_count, total_rows, last_updated)
    VALUES (
        NEW.query_id,
        NEW.execution_time,
        NEW.execution_time,
        NEW.execution_time,
        1,
        NEW.rows_returned,
        CURRENT_TIMESTAMP
    )
    ON CONFLICT (query_id)
    DO UPDATE SET
        avg_execution_time = (
            query_aggregates.avg_execution_time * query_aggregates.execution_count + NEW.execution_time
        ) / (query_aggregates.execution_count + 1),
        max_execution_time = GREATEST(query_aggregates.max_execution_time, NEW.execution_time),
        min_execution_time = LEAST(query_aggregates.min_execution_time, NEW.execution_time),
        execution_count = query_aggregates.execution_count + 1,
        total_rows = query_aggregates.total_rows + NEW.rows_returned,
        last_updated = CURRENT_TIMESTAMP;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_aggregates
AFTER INSERT ON query_executions
FOR EACH ROW
EXECUTE FUNCTION update_query_aggregates();
