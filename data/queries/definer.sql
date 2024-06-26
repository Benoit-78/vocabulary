
------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure

-- Databases
CREATE DATABASE vocabulary;
CREATE DATABASE users;

DROP DATABASE <database_name>;

SHOW DATABASES;


-- Tables
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);

SHOW TABLES;

RENAME TABLE zhongwen.theme_perf TO benoit_zhongwen.theme_perf;

DESCRIBE version_voc;

SHOW COLUMNS FROM version_voc;

DROP TABLE <table_name>;
