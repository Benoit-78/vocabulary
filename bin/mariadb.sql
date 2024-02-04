
-----------------------
-- BASH INSTRUCTIONS --
-----------------------
cd ~/vocabulary/data
sudo mariadb
sudo systemctl restart mariadb


---------------------------
-- Data Control Language --
---------------------------
-- Manage access and transactions
-- Ex: GRANT, REVOKE, COMMIT, ROLLBACK

-- root user
CREATE USER 'root'@'localhost' IDENTIFIED BY '<db_password>';

ALTER USER 'usr'@'%' IDENTIFIED BY 'pwd';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'IBM-vocabulary7' WITH GRANT OPTION;


-- guests
GRANT ALL PRIVILEGES ON vocabulary.* TO 'guest'@'localhost';

REVOKE ALL PRIVILEGES ON `vocabulary`.* FROM `guest`@`localhost`;


-- users
GRANT CREATE, SELECT, INSERT, UPDATE, DROP ON theme_perf TO '<user-name>'@'localhost';

DROP USER 'usr'@'%';
DROP USER 'usr'@'localhost';

-- Very very useful
FLUSH PRIVILEGES;



------------------------------
-- Data Definition Language --
------------------------------
-- Define database structure
-- Ex: CREATE, ALTER, DROP

-- Databases
CREATE DATABASE vocabulary;

DROP DATABASE <database_name>;

-- Tables
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);

RENAME TABLE zhongwen.theme_perf TO benoit_zhongwen.theme_perf;



--------------------------------
-- Data Manipulation Language --
--------------------------------
-- Working with data
-- Ex: SELECT, INSERT, UPDATE, DELETE

-- Write
INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES (2, '2022-10-29', 83);

LOAD DATA INFILE '/path/data.txt' INTO TABLE your_table
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    (column1, column2, @percentage_variable)
    SET percentage = CAST(@percentage_variable AS SIGNED);




