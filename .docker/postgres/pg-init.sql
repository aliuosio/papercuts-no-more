-- Clear collation versions for Alpine PostgreSQL compatibility
-- This prevents the WARNING: database has no actual collation version, but a version was recorded
UPDATE pg_catalog.pg_database SET datcollversion = NULL WHERE datcollversion IS NOT NULL;
