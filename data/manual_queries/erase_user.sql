
-- Erase
SET @username = 'usr_4';
SET @query = CONCAT('DROP USER ', @username, '@localhost');
PREPARE stmt FROM @query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
DELETE FROM users.voc_users WHERE username = @username;
DELETE FROM mysql.user WHERE User = @username;

-- check
SELECT host, user, authentication_string FROM mysql.user WHERE authentication_string IS NOT NULL;
SELECT * FROM users.voc_users;