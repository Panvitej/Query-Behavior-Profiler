// ======================================================
// QUERY PROFILER - MONGODB SETUP
// Run using: mongosh < mongo_schema.js
// ======================================================

// Switch to database
use query_profiler;


// ==============================
// COLLECTION CREATION
// ==============================
db.createCollection("query_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["query_text", "normalized_query", "execution_time", "created_at"],
      properties: {
        query_text: {
          bsonType: "string",
          description: "Original SQL query"
        },
        normalized_query: {
          bsonType: "string",
          description: "Normalized query for grouping"
        },
        execution_time: {
          bsonType: "double",
          description: "Execution time in seconds"
        },
        rows_returned: {
          bsonType: "int",
          description: "Rows returned by query"
        },
        cpu_time: {
          bsonType: ["double", "null"],
          description: "CPU time used"
        },
        memory_usage: {
          bsonType: ["double", "null"],
          description: "Memory usage in MB"
        },
        created_at: {
          bsonType: "date",
          description: "Timestamp of execution"
        }
      }
    }
  }
});


// ==============================
// INDEXES (CRITICAL)
// ==============================

// Query grouping
db.query_logs.createIndex(
  { normalized_query: 1 },
  { name: "idx_normalized_query" }
);

// Execution time analysis
db.query_logs.createIndex(
  { execution_time: -1 },
  { name: "idx_execution_time_desc" }
);

// Time-based queries
db.query_logs.createIndex(
  { created_at: -1 },
  { name: "idx_created_at_desc" }
);

// Compound index (IMPORTANT)
db.query_logs.createIndex(
  { normalized_query: 1, execution_time: -1 },
  { name: "idx_query_time" }
);

// Time-series optimization
db.query_logs.createIndex(
  { normalized_query: 1, created_at: -1 },
  { name: "idx_query_time_series" }
);


// ==============================
// TTL INDEX (AUTO CLEANUP)
// ==============================

// Delete logs older than 7 days
db.query_logs.createIndex(
  { created_at: 1 },
  {
    expireAfterSeconds: 604800,
    name: "ttl_7_days"
  }
);


// ==============================
// SAMPLE AGGREGATION PIPELINE
// ==============================

// Example: Average execution time per query
db.query_logs.aggregate([
  {
    $group: {
      _id: "$normalized_query",
      avg_time: { $avg: "$execution_time" },
      max_time: { $max: "$execution_time" },
      count: { $sum: 1 }
    }
  },
  {
    $sort: { avg_time: -1 }
  }
]);


// ==============================
// PERFORMANCE CHECK
// ==============================

// Check indexes
db.query_logs.getIndexes();

// Check collection stats
db.query_logs.stats();
