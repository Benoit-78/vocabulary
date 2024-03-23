
CREATE DATABASE voc_users;
USE voc_users;



---------------------------
--  D E F I N I T I O N  --
---------------------------
CREATE TABLE voc_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    email VARCHAR(100),
    disabled BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


---------------------
--  C O N T R O L  --
---------------------
-- If through uvicorn: localhost
-- If through a container: db
GRANT SELECT ON voc_users TO 'root'@'localhost';



-------------------------------
--  M A N I P U L A T I O N  --
-------------------------------
INSERT INTO `users`.`voc_users` (`username`, `password_hash`, `email`, `disabled`) VALUES
    ('wh0Are_y0u', '*DA6C14463E14177A0621A25F264C2AED66E5A2F4', '', FALSE);

SELECT username FROM `users`.`voc_users`;