
-----------------------
-- BASH INSTRUCTIONS --
-----------------------
-- cd ~/vocabulary/data
-- sudo mariadb



---------------------------
-- Data Control Language --
---------------------------
SELECT host, user, password FROM mysql.user;

CREATE USER 'benoit'@'localhost' IDENTIFIED BY '<db_password>';

ALTER USER 'benoit'@'localhost' IDENTIFIED BY '<db_password>';

SHOW GRANTS FOR 'benoit'@'localhost';

GRANT ALL PRIVILEGES ON {new_database_name}.* TO 'benoit'@'localhost'

GRANT CREATE, SELECT, INSERT, UPDATE, DROP ON theme_perf TO 'benoit'@'localhost';



------------------------------
-- Data Definition Language --
------------------------------
SHOW DATABASES;

SHOW TABLES;

DESCRIBE version_voc;

SHOW COLUMNS FROM version_voc;

CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);

DROP DATABASE <database_name>;

RENAME TABLE zhongwen.theme_perf TO benoit_zhongwen.theme_perf;



--------------------------------
-- Data Manipulation Language --
--------------------------------
INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES (2, '2022-10-29', 83);

LOAD DATA INFILE '/path/data.txt' INTO TABLE your_table
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(column1, column2, @percentage_variable)
SET percentage = CAST(@percentage_variable AS SIGNED);



------------
-- Others --
------------
USE english;

SOURCE english.sql;
