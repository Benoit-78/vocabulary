---------------------------
-- Data Control Language --
---------------------------
-- Manage access

SELECT host, user, password FROM mysql.user;

SHOW GRANTS FOR 'root'@'localhost';

SHOW ENGINES;

SHOW ERRORS;

-- Hosts
SELECT host, statements, statement_avg_latency, table_scans, file_ios, file_io_latency, total_connections, unique_users, total_memory_allocated
FROM sys.host_summary;

-- Users
SELECT * FROM sys.memory_by_user_by_current_bytes;

SELECT user, statements, statement_avg_latency, table_scans, file_ios, file_io_latency, total_connections, unique_hosts, total_memory_allocated
FROM sys.user_summary;

-- Queries
SELECT query, db, exec_count, total_latency, last_seen
FROM sys.statements_with_sorting
ORDER BY exec_count DESC
LIMIT 10;



------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure
SHOW DATABASES;

SHOW TABLES;

DESCRIBE version_voc;

SHOW COLUMNS FROM version_voc;



--------------------------------
-- Data Manipulation Language --
--------------------------------
-- Working with data
-- Ex: SELECT, INSERT, UPDATE, DELETE

-- Read
SELECT * FROM column_1, column_2;



-------------------------------
-- MariaDB-specific commands --
------------------------------
USE english;

SOURCE english.sql;
