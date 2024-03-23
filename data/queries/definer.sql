
------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure

-- Databases
CREATE DATABASE vocabulary;
CREATE DATABASE users;

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
