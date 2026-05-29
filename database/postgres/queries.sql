-- PostgreSQL query patterns
-- Covers: CTEs, window functions, JSONB, full-text search, upsert, explain

-- ---------------------------------------------------------------------------
-- Pagination (keyset — faster than OFFSET on large tables)
-- ---------------------------------------------------------------------------

-- First page
SELECT id, title, status, created_at
FROM items
WHERE project_id = 'PROJECT-UUID'
  AND status = 'active'
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Next page (pass last row's created_at + id as cursor)
SELECT id, title, status, created_at
FROM items
WHERE project_id = 'PROJECT-UUID'
  AND status = 'active'
  AND (created_at, id) < ('2026-01-15T10:00:00Z', 'LAST-UUID')
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- ---------------------------------------------------------------------------
-- Full-text search (trigram — handles partial matches, typos)
-- ---------------------------------------------------------------------------

SELECT id, title, similarity(title, 'deploy pipeline') AS score
FROM items
WHERE title % 'deploy pipeline'    -- trigram similarity threshold (default 0.3)
ORDER BY score DESC
LIMIT 10;

-- Full-text search (tsvector — language-aware, better for long text)
SELECT id, title, body,
  ts_rank(to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(body, '')),
          plainto_tsquery('english', 'kubernetes deployment')) AS rank
FROM items
WHERE to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(body, ''))
      @@ plainto_tsquery('english', 'kubernetes deployment')
ORDER BY rank DESC;

-- ---------------------------------------------------------------------------
-- JSONB queries
-- ---------------------------------------------------------------------------

-- Exact key match
SELECT id, metadata->>'env' AS env
FROM items
WHERE metadata @> '{"env": "production"}';

-- Nested path
SELECT id, metadata #>> '{labels, team}' AS team
FROM items
WHERE metadata #> '{labels}' ? 'team';

-- Array contains
SELECT id FROM items
WHERE metadata @> '{"tags": ["critical"]}';

-- Update nested key without overwriting whole object
UPDATE items
SET metadata = metadata || '{"reviewed": true}'::JSONB
WHERE id = 'ITEM-UUID';

-- ---------------------------------------------------------------------------
-- CTEs
-- ---------------------------------------------------------------------------

WITH
project_stats AS (
  SELECT
    project_id,
    COUNT(*)                                           AS total,
    COUNT(*) FILTER (WHERE status = 'active')          AS active,
    AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) AS avg_age_seconds
  FROM items
  GROUP BY project_id
),
top_projects AS (
  SELECT project_id FROM project_stats
  ORDER BY active DESC
  LIMIT 10
)
SELECT p.name, ps.total, ps.active,
       ROUND(ps.avg_age_seconds / 3600, 1) AS avg_age_hours
FROM projects p
JOIN project_stats ps ON ps.project_id = p.id
JOIN top_projects tp  ON tp.project_id = p.id
ORDER BY ps.active DESC;

-- ---------------------------------------------------------------------------
-- Window functions
-- ---------------------------------------------------------------------------

-- Rank items within each project by recency
SELECT
  id,
  project_id,
  title,
  created_at,
  ROW_NUMBER()   OVER (PARTITION BY project_id ORDER BY created_at DESC) AS recency_rank,
  COUNT(*)       OVER (PARTITION BY project_id)                           AS project_total,
  LAG(title, 1) OVER (PARTITION BY project_id ORDER BY created_at)      AS previous_title
FROM items
WHERE status = 'active';

-- Running total per owner
SELECT
  owner_id,
  created_at::DATE AS day,
  COUNT(*)         AS daily_items,
  SUM(COUNT(*)) OVER (PARTITION BY owner_id ORDER BY created_at::DATE) AS running_total
FROM items
GROUP BY owner_id, day
ORDER BY owner_id, day;

-- ---------------------------------------------------------------------------
-- Upsert
-- ---------------------------------------------------------------------------

INSERT INTO users (email, name, role)
VALUES ('alice@example.com', 'Alice Smith', 'editor')
ON CONFLICT (email) DO UPDATE
  SET name       = EXCLUDED.name,
      role       = EXCLUDED.role,
      updated_at = NOW()
RETURNING id, email, role;

-- ---------------------------------------------------------------------------
-- Bulk insert with returning
-- ---------------------------------------------------------------------------

INSERT INTO items (project_id, owner_id, title, status)
SELECT
  'PROJECT-UUID',
  'OWNER-UUID',
  'Item ' || n,
  'draft'
FROM generate_series(1, 100) AS n
RETURNING id, title;

-- ---------------------------------------------------------------------------
-- EXPLAIN / performance
-- ---------------------------------------------------------------------------

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT i.id, i.title, u.name AS owner
FROM items i
JOIN users u ON u.id = i.owner_id
WHERE i.project_id = 'PROJECT-UUID'
  AND i.status = 'active'
ORDER BY i.created_at DESC
LIMIT 20;

-- Check index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
WHERE tablename IN ('items', 'users', 'projects')
ORDER BY idx_scan DESC;

-- Find slow queries (requires pg_stat_statements extension)
-- CREATE EXTENSION pg_stat_statements;
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
