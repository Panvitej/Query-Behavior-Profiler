# Query Behavior Profiler

A hybrid system for analyzing SQL query performance using:

- MongoDB (raw query logging)
- Python (processing + analysis)
- PostgreSQL (analytics engine)

---

## Overview

This project implements a query profiling system that captures SQL query behavior, analyzes performance patterns, and generates optimization insights.

It separates concerns across three layers:

- **MongoDB** → ingestion (raw logs)
- **Python** → processing and analytics
- **PostgreSQL** → structured analytical storage

---

## System Flow
Query Execution
↓
MongoDB (raw logs)
↓
Python processing (normalization + analysis)
↓
PostgreSQL (aggregated analytics)
↓
Insights + optimization suggestions


---

## Project Structure

```bash
query-profiler/
│
├── app/
│   ├── core.py
│   ├── parser.py
│   ├── engine.py
│   └── sync.py
│
├── sql/
│   └── schema.sql
│
├── mongo/
│   └── mongo_schema.js
│
├── config/
│   └── settings.py
│
├── requirements.txt
├── run.py
└── README.md
```
---

## Components

### 1. MongoDB (Ingestion Layer)

- Stores raw query logs
- Flexible schema
- High write performance

Each document contains:
query_text
normalized_query
execution_time
rows_returned
created_at


Indexes ensure fast lookup and time-based queries.

---

### 2. Python (Processing Layer)

Handles:

- Query normalization
- Fingerprinting
- Feature extraction
- Performance analysis
- Optimization suggestions

Key modules:

core.py → MongoDB interaction
parser.py → query normalization
engine.py → analysis logic
sync.py → Mongo → PostgreSQL pipeline


---

### 3. PostgreSQL (Analytics Layer)

Stores structured and aggregated data:

- Query statistics
- Execution metrics
- Time-series data

Optimized using:

- Indexes
- Materialized views
- Aggregation tables

---

## Setup Instructions

### 1. Install Dependencies

pip install -r requirements.txt

---

### 2. Start MongoDB


mongod

---

### 3. Initialize MongoDB


mongosh < mongo/mongo_schema.js


---

### 4. Setup PostgreSQL

Create database:


createdb query_profiler


Apply schema:


psql -d query_profiler -f sql/schema.sql


---

### 5. Configure Settings

Edit:


config/settings.py

Set:

- MongoDB URI
- PostgreSQL credentials

---

### 6. Run System


python run.py


---

## What Happens on Run


Queries are simulated

Logs are stored in MongoDB

Python analyzes performance

Aggregated data is pushed to PostgreSQL

Insights are printed


---

## Analysis Capabilities

The system detects:

- Slow queries
- Frequently executed queries
- Execution time spikes
- Query patterns
- Basic optimization opportunities

---

## Example Output


=== Slow Queries ===
...

=== Frequent Queries ===
...

=== Optimization Suggestions ===
SELECT * FROM users WHERE id = ?
→ Avoid SELECT *
→ Add index on WHERE column


---

## Design Decisions

### MongoDB

Used for:

- High-speed ingestion
- Flexible schema
- Logging large volumes of data

---

### PostgreSQL

Used for:

- Structured analytics
- Aggregation
- Index-based querying

---

### Python

Used for:

- Data transformation
- Analysis logic
- ETL pipeline

---

## Performance Considerations

- Indexed query normalization
- Time-based indexing
- Aggregated metrics
- Reduced scan overhead in SQL layer

---

## Limitations

- Uses simulated queries (not real DB logs yet)
- Batch processing (not real-time)
- Basic rule-based optimizer

---

## Future Improvements

- Real-time ingestion pipeline
- Query plan analysis (EXPLAIN ANALYZE)
- Machine learning anomaly detection
- REST API (FastAPI)
- Dashboard (Streamlit / Grafana)

---

## Resume Summary

Built a hybrid query profiling system using MongoDB for ingestion and PostgreSQL for analytical processing, with a Python-based pipeline for query normalization, performance analysis, and optimization.

---

## License

MIT


