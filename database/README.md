# Database

Schema and query reference examples.

## Directories

| Directory | Covers |
|-----------|--------|
| [`postgres/`](postgres/) | Schema DDL, indexes, RLS, partitioning, CTEs, window functions, JSONB, full-text search |
| [`mongodb/`](mongodb/) | CRUD, aggregation pipeline, schema validation, indexes, transactions, text search |

---

## PostgreSQL

**Files:** [`postgres/schema.sql`](postgres/schema.sql) · [`postgres/queries.sql`](postgres/queries.sql)

```bash
# Apply schema to a local database
psql $DATABASE_URL -f database/postgres/schema.sql

# Run example queries (read-only — safe against any dataset)
psql $DATABASE_URL -f database/postgres/queries.sql
```

**Patterns covered:**
- Extensions: `pgcrypto` (UUIDs), `pg_trgm` (trigram search), `btree_gin`
- Enums, domains (email, slug)
- `updated_at` trigger (shared function)
- GIN / trigram indexes for fast LIKE/similarity search
- JSONB querying and partial updates
- Keyset pagination (faster than OFFSET on large tables)
- CTEs and window functions
- Upsert (`ON CONFLICT DO UPDATE`)
- Row-level security (RLS)
- Range partitioning for time-series events
- `EXPLAIN ANALYZE` + `pg_stat_statements` patterns

---

## MongoDB

**File:** [`mongodb/examples.py`](mongodb/examples.py)

```bash
pip install pymongo python-dotenv
python database/mongodb/examples.py
python database/mongodb/examples.py --demo-write
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URI` | `mongodb://localhost:27017` | Connection URI (supports Atlas URIs) |
| `MONGODB_DB` | `myapp` | Database name |

**Patterns covered:**
- Collection creation with JSON Schema validation
- Single, compound, text, and TTL indexes
- CRUD with `find_one_and_update`, `$set`, `$all`
- Text search (`$text`) with field weights
- Aggregation pipeline: `$group`, `$lookup`, `$unwind`, `$project`
- Multi-document transactions (client sessions)
- `--demo-write` creates users + items, runs aggregation, cleans up
