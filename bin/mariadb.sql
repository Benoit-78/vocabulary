

-- Bash commands
cd ~/vocabulary/data
sudo mariadb -u root -p
sudo systemctl restart mariadb

-- MariaDB-specific commands
USE english;

SOURCE english.sql;

system clear;



---------------------------
-- Data Control Language --
---------------------------
-- Manage access and transactions

-- root user
CREATE USER 'root'@'localhost' IDENTIFIED BY '<db_password>';

ALTER USER 'usr'@'localhost' IDENTIFIED BY 'pwd';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '<pwd>' WITH GRANT OPTION;

GRANT SELECT ON common.* TO '%'@'%';

-- guests
CREATE USER 'wh0Are_y0u'@'localhost' IDENTIFIED BY 'AnIs0tr0p|';

GRANT SELECT ON vocabulary.* TO 'wh0Are_y0u'@'localhost';

SHOW GRANTS FOR 'wh0Are_y0u'@'localhost';

REVOKE CREATE ON vocabulary.* FROM `wh0Are_y0u`@`localhost`;

DROP USER 'wh0Are_y0u'@'localhost';

-- users
SELECT host, user password FROM mysql.user;

GRANT CREATE, SELECT, INSERT, UPDATE, DROP ON theme_perf TO '<user-name>'@'localhost';

DROP USER 'usr'@'%';
DROP USER 'usr'@'localhost';

SELECT * FROM sys.memory_by_user_by_current_bytes;

SELECT user, statements, statement_avg_latency, table_scans, file_ios, file_io_latency, total_connections, unique_hosts, total_memory_allocated
FROM sys.user_summary;

-- Very very useful
FLUSH PRIVILEGES;

-- Manage access
SELECT User FROM mysql.db WHERE Db = 'mysql';

SHOW ENGINES;

SHOW ERRORS;

-- Hosts
SELECT host, statements, statement_avg_latency, table_scans, file_ios, file_io_latency, total_connections, unique_users, total_memory_allocated
FROM sys.host_summary;

-- Management queries
SELECT query, db, exec_count, total_latency, last_seen
FROM sys.statements_with_sorting
ORDER BY exec_count DESC
LIMIT 10;


------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure

-- Databases
CREATE DATABASE vocabulary;

DROP DATABASE <database_name>;

-- Tables
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);

RENAME TABLE zhongwen.theme_perf TO benoit_zhongwen.theme_perf;

SHOW DATABASES;

SHOW TABLES;

DESCRIBE version_voc;

SHOW COLUMNS FROM version_voc;

--------------------------------
-- Data Manipulation Language --
--------------------------------
-- Working with data

-- Write
INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES (2, '2022-10-29', 83);

LOAD DATA INFILE '/path/data.txt' INTO TABLE your_table
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    (column1, column2, @percentage_variable)
    SET percentage = CAST(@percentage_variable AS SIGNED);
