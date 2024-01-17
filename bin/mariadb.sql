
-----------------------
-- BASH INSTRUCTIONS --
-----------------------
-- cd ~/vocabulary/data
-- sudo mariadb



---------------------------
-- Data Control Language --
---------------------------
-- Manage access and transactions
-- Ex: GRANT, REVOKE, COMMIT, ROLLBACK

SELECT host, user, password FROM mysql.user;

CREATE USER 'benoit'@'localhost' IDENTIFIED BY '<db_password>';

ALTER USER 'benoit'@'localhost' IDENTIFIED BY '<db_password>';

SHOW GRANTS FOR 'benoit'@'localhost';

GRANT ALL PRIVILEGES ON {new_database_name}.* TO 'benoit'@'localhost'

GRANT CREATE, SELECT, INSERT, UPDATE, DROP ON theme_perf TO 'benoit'@'localhost';

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
SELECT query, db, exec_count, total_latency, last_seen FROM sys.statements_with_sorting
ORDER BY exec_count DESC
LIMIT 10;


------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure
-- Ex: CREATE, ALTER, DROP

-- Databases
CREATE DATABASE db_name;

DROP DATABASE <database_name>;

SHOW DATABASES;

-- Tables
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);

RENAME TABLE zhongwen.theme_perf TO benoit_zhongwen.theme_perf;

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

-- Write
INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES (2, '2022-10-29', 83);

LOAD DATA INFILE '/path/data.txt' INTO TABLE your_table
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    (column1, column2, @percentage_variable)
    SET percentage = CAST(@percentage_variable AS SIGNED);



-------------------------------
-- MariaDB-specific commands --
------------------------------
USE english;

SOURCE english.sql;
