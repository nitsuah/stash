-- PostgreSQL schema reference
-- Patterns: extensions, enums, domains, tables, indexes, foreign keys,
--           triggers (updated_at), views, RLS, partitioning

-- ---------------------------------------------------------------------------
-- Extensions
-- ---------------------------------------------------------------------------

CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- trigram indexes for LIKE search
CREATE EXTENSION IF NOT EXISTS "btree_gin";  -- GIN indexes on scalar types

-- ---------------------------------------------------------------------------
-- Enums
-- ---------------------------------------------------------------------------

CREATE TYPE user_role AS ENUM ('admin', 'editor', 'viewer');
CREATE TYPE item_status AS ENUM ('draft', 'active', 'archived');
CREATE TYPE event_type AS ENUM ('created', 'updated', 'deleted', 'transitioned');

-- ---------------------------------------------------------------------------
-- Domains (reusable constraints)
-- ---------------------------------------------------------------------------

CREATE DOMAIN email AS TEXT
  CHECK (VALUE ~* '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$');

CREATE DOMAIN slug AS TEXT
  CHECK (VALUE ~* '^[a-z0-9][a-z0-9\-]{0,62}[a-z0-9]$');

-- ---------------------------------------------------------------------------
-- updated_at trigger function (shared)
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

-- ---------------------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------------------

CREATE TABLE users (
  id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  email       email        NOT NULL,
  name        TEXT         NOT NULL CHECK (char_length(name) BETWEEN 1 AND 255),
  role        user_role    NOT NULL DEFAULT 'viewer',
  active      BOOLEAN      NOT NULL DEFAULT TRUE,
  metadata    JSONB        NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

  CONSTRAINT users_email_unique UNIQUE (email)
);

CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Trigram index for fast name/email search
CREATE INDEX idx_users_email_trgm ON users USING GIN (email gin_trgm_ops);
CREATE INDEX idx_users_name_trgm  ON users USING GIN (name  gin_trgm_ops);
CREATE INDEX idx_users_active     ON users (active) WHERE active = TRUE;


CREATE TABLE teams (
  id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  slug        slug         NOT NULL,
  name        TEXT         NOT NULL,
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

  CONSTRAINT teams_slug_unique UNIQUE (slug)
);

CREATE TRIGGER teams_updated_at
  BEFORE UPDATE ON teams
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();


CREATE TABLE team_members (
  team_id    UUID       NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  user_id    UUID       NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role       user_role  NOT NULL DEFAULT 'viewer',
  joined_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  PRIMARY KEY (team_id, user_id)
);

CREATE INDEX idx_team_members_user ON team_members (user_id);


CREATE TABLE projects (
  id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id     UUID         NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  slug        slug         NOT NULL,
  name        TEXT         NOT NULL,
  description TEXT,
  settings    JSONB        NOT NULL DEFAULT '{}',
  created_by  UUID         NOT NULL REFERENCES users(id),
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

  CONSTRAINT projects_team_slug_unique UNIQUE (team_id, slug)
);

CREATE TRIGGER projects_updated_at
  BEFORE UPDATE ON projects
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX idx_projects_team ON projects (team_id);


CREATE TABLE items (
  id          UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id  UUID         NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  owner_id    UUID         NOT NULL REFERENCES users(id),
  title       TEXT         NOT NULL CHECK (char_length(title) BETWEEN 1 AND 255),
  body        TEXT,
  status      item_status  NOT NULL DEFAULT 'draft',
  tags        TEXT[]       NOT NULL DEFAULT '{}',
  position    INTEGER      NOT NULL DEFAULT 0,
  metadata    JSONB        NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TRIGGER items_updated_at
  BEFORE UPDATE ON items
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE INDEX idx_items_project        ON items (project_id);
CREATE INDEX idx_items_owner          ON items (owner_id);
CREATE INDEX idx_items_status         ON items (project_id, status);
CREATE INDEX idx_items_tags           ON items USING GIN (tags);
CREATE INDEX idx_items_metadata       ON items USING GIN (metadata jsonb_path_ops);
CREATE INDEX idx_items_title_trgm     ON items USING GIN (title gin_trgm_ops);
CREATE INDEX idx_items_position       ON items (project_id, position);


-- Audit / event log (append-only)
CREATE TABLE audit_log (
  id          BIGSERIAL    PRIMARY KEY,
  table_name  TEXT         NOT NULL,
  record_id   UUID         NOT NULL,
  event       event_type   NOT NULL,
  actor_id    UUID         REFERENCES users(id) ON DELETE SET NULL,
  old_data    JSONB,
  new_data    JSONB,
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_record   ON audit_log (table_name, record_id);
CREATE INDEX idx_audit_actor    ON audit_log (actor_id);
CREATE INDEX idx_audit_time     ON audit_log (created_at DESC);

-- ---------------------------------------------------------------------------
-- Views
-- ---------------------------------------------------------------------------

-- Active users with team count
CREATE VIEW v_active_users AS
SELECT
  u.id,
  u.email,
  u.name,
  u.role,
  u.created_at,
  COUNT(tm.team_id) AS team_count
FROM users u
LEFT JOIN team_members tm ON tm.user_id = u.id
WHERE u.active = TRUE
GROUP BY u.id;

-- Project summary with counts
CREATE VIEW v_project_summary AS
SELECT
  p.id,
  p.team_id,
  p.slug,
  p.name,
  p.created_at,
  COUNT(i.id)                                           AS item_count,
  COUNT(i.id) FILTER (WHERE i.status = 'active')        AS active_count,
  COUNT(i.id) FILTER (WHERE i.status = 'draft')         AS draft_count,
  COUNT(i.id) FILTER (WHERE i.status = 'archived')      AS archived_count,
  MAX(i.updated_at)                                     AS last_activity
FROM projects p
LEFT JOIN items i ON i.project_id = p.id
GROUP BY p.id;

-- ---------------------------------------------------------------------------
-- Row-level security (RLS)
-- ---------------------------------------------------------------------------
-- Enable after connecting app role; app sets: SET app.current_user_id = '<uuid>'

ALTER TABLE items ENABLE ROW LEVEL SECURITY;

CREATE POLICY items_select ON items
  FOR SELECT USING (
    owner_id = current_setting('app.current_user_id', TRUE)::UUID
    OR project_id IN (
      SELECT p.id FROM projects p
      JOIN team_members tm ON tm.team_id = p.team_id
      WHERE tm.user_id = current_setting('app.current_user_id', TRUE)::UUID
    )
  );

CREATE POLICY items_insert ON items
  FOR INSERT WITH CHECK (
    owner_id = current_setting('app.current_user_id', TRUE)::UUID
  );

CREATE POLICY items_update ON items
  FOR UPDATE USING (
    owner_id = current_setting('app.current_user_id', TRUE)::UUID
  );

CREATE POLICY items_delete ON items
  FOR DELETE USING (
    owner_id = current_setting('app.current_user_id', TRUE)::UUID
  );

-- ---------------------------------------------------------------------------
-- Partitioned table example (time-series events)
-- ---------------------------------------------------------------------------

CREATE TABLE events (
  id         BIGSERIAL,
  project_id UUID         NOT NULL,
  type       TEXT         NOT NULL,
  payload    JSONB        NOT NULL DEFAULT '{}',
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (occurred_at);

-- Monthly partitions (create as needed; automate with pg_partman in prod)
CREATE TABLE events_2026_01 PARTITION OF events
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE events_2026_02 PARTITION OF events
  FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE INDEX idx_events_project ON events (project_id, occurred_at DESC);

-- ---------------------------------------------------------------------------
-- Seed data (dev only)
-- ---------------------------------------------------------------------------

INSERT INTO users (email, name, role) VALUES
  ('alice@example.com', 'Alice',   'admin'),
  ('bob@example.com',   'Bob',     'editor'),
  ('carol@example.com', 'Carol',   'viewer')
ON CONFLICT (email) DO NOTHING;

INSERT INTO teams (slug, name) VALUES
  ('platform', 'Platform Engineering'),
  ('product',  'Product')
ON CONFLICT (slug) DO NOTHING;
