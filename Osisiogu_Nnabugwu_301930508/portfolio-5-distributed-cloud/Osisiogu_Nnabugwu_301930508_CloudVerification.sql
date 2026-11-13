-- PROPOSED / UNTESTED cloud check. Read-only; uses externally supplied libpq settings.
-- Run with PGSSLMODE=verify-full, trusted RDS CA and protected authentication.
BEGIN READ ONLY;
SELECT current_database() AS database_name, current_user AS connected_role,
       current_setting('server_version') AS server_version,
       pg_is_in_recovery() AS is_replica;
SELECT ssl, version AS tls_version, cipher
FROM pg_stat_ssl WHERE pid = pg_backend_pid();
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_stat_ssl WHERE pid = pg_backend_pid() AND ssl) THEN
        RAISE EXCEPTION 'TLS is not active for this connection';
    END IF;
END $$;
ROLLBACK;
