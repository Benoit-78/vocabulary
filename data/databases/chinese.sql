-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           11.2.0-MariaDB - mariadb.org binary distribution
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- If localhost
CREATE DATABASE wh0_Are_y0u_chinese;
USE wh0_Are_y0u_chinese;


-------------------------------------
--  T A B L E S   C R E A T I O N  --
-------------------------------------
CREATE TABLE IF NOT EXISTS version_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT
);

CREATE TABLE IF NOT EXISTS version_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    zhongwen CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
	pinyin VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255),
	creation_date DATE,
	nb TINYINT,
	score TINYINT,
	taux TINYINT
);

CREATE TABLE IF NOT EXISTS version_words_count (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
	words_count SMALLINT
);


CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT
);

CREATE TABLE IF NOT EXISTS theme_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    zhongwen CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
	pinyin VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255),
	creation_date DATE,
	nb TINYINT,
	score TINYINT,
	taux DOUBLE
);

CREATE TABLE IF NOT EXISTS theme_words_count (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
	words_count SMALLINT
);

CREATE TABLE IF NOT EXISTS archive (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    zhongwen CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
	pinyin VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255)
);


-------------------------------------------
--  T A B L E S   P E R M I S S I O N S  --
-------------------------------------------
-- If through uvicorn: localhost
-- If through a container: db
GRANT SELECT ON theme_perf TO 'wh0_Are_y0u'@'localhost';
GRANT SELECT ON theme_voc TO 'wh0_Are_y0u'@'localhost';
GRANT SELECT ON theme_words_count TO 'wh0_Are_y0u'@'localhost';

GRANT SELECT ON version_perf TO 'wh0_Are_y0u'@'localhost';
GRANT SELECT ON version_voc TO 'wh0_Are_y0u'@'localhost';
GRANT SELECT ON version_words_count TO 'wh0_Are_y0u'@'localhost';

GRANT SELECT ON archive TO 'wh0_Are_y0u'@'localhost';



-----------------------------------
--  T A B L E S   F I L L I N G  --
-----------------------------------
INSERT INTO `version_perf` (`id_test`, `test_date`, `test`) VALUES
	(1, '1991-12-03', 0);

INSERT INTO `version_voc` (`id_word`, `zhongwen`, `pinyin`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
	(1, '汉语', 'Hàn yǔ', 'Langue chinoise', '2023-11-12', 0, 0, 0),
	(2, '开', 'Kāi', 'Ouvrir', '2023-11-12', 0, 0, 0),
	(3, '门', 'Mén', 'Porte', '2023-11-12', 0, 0, 0),
	(4, '麻烦', 'Máfan', 'Déranger', '2023-11-12', 0, 0, 0),
	(5,'爸爸', 'BàBà', 'Papa', '2023-11-12', 0, 0, 0),
	(6, '妈妈', 'Māmā', 'Maman', '2023-11-12', 0, 0, 0),
	(7, '爸妈', 'Bàmā', 'Mes parents', '2023-11-12', 0, 0, 0),
	(8, '你', 'Nǐ', 'Toi', '2023-11-12', 0, 0, 0),
	(9, '好', 'hǎo', 'Bon, bien', '2023-11-12', 0, 0, 0),
	(10, '是', 'Shì', 'Être', '2023-11-12', 0, 0, 0),
	(11, '吗', 'Ma', 'Terminaison interrogative', '2023-11-12', 0, 0, 0),
	(12, '爱', 'Ài', 'Aimer', '2023-11-12', 0, 0, 0),
	(13, '吃', 'Chī', 'Manger', '2023-11-12', 0, 0, 0),
	(14, '呢', 'ne', 'Particule interrogative', '2023-11-12', 0, 0, 0),
	(15, '也', 'yě', 'Aussi', '2023-11-12', 0, 0, 0),
	(16, '鱼', 'Yú', 'Poisson', '2023-11-12', 0, 0, 0),
	(17, '喝', 'Hē', 'Boire', '2023-11-12', 0, 0, 0),
	(18, '汤', 'Tāng', 'Soupe', '2023-11-12', 0, 0, 0),
	(19, '他', 'Tā', 'Il', '2023-11-12', 0, 0, 0),
	(20, '她', 'Tā', 'Elle', '2023-11-12', 0, 0, 0),
	(21, '茶', 'chá', 'Thé', '2023-11-12', 0, 0, 0),
	(22, '累', 'lèi', 'Fatigué', '2023-11-12', 0, 0, 0),
	(23, '饿', 'è', 'Avoir faim', '2023-11-12', 0, 0, 0),
	(24, '渴', 'kě', 'Avoir soif', '2023-11-12', 0, 0, 0),
	(25, '不', 'bù', 'Signe de la négation', '2023-11-12', 0, 0, 0),
	(26, '很', 'hěn', 'Très', '2023-11-12', 0, 0, 0),
	(27, '要', 'yào', 'Vouloir', '2023-11-12', 0, 0, 0),
	(28, '什么', 'shénme', 'quoi', '2023-11-12', 0, 0, 0),
	(30, '绿', 'lǜ', 'vert', '2023-11-12', 0, 0, 0),
	(31, '谢谢', 'xiè xiè', 'merci', '2023-11-12', 0, 0, 0),
	(32, '男', 'nán', 'masculin, homme', '2023-11-12', 0, 0, 0),
	(33, '朋友', 'péng yǒu', 'ami', '2023-11-12', 0, 0, 0),
	(34, '谁', 'shéi', 'qui', '2023-11-12', 0, 0, 0),
	(35, '哥哥', 'gēgē', 'grand frère', '2023-11-12', 0, 0, 0),
	(36, '弟弟', 'dìdì', 'Petit frère', '2023-11-12', 0, 0, 0),
	(37, '帅', 'shuài', 'beau', '2023-11-12', 0, 0, 0),
	(38, '女', 'Nǚ', 'femme', '2023-11-12', 0, 0, 0),
	(39, '有', 'Yǒu', 'il y a', '2023-11-12', 0, 0, 0),
	(40, '没有', 'Méiyǒu', 'il n’y a pas', '2023-11-12', 0, 0, 0),
	(41, '贵', 'guì', 'cher', '2023-11-12', 0, 0, 0),
	(42, '看', 'kàn', 'Regarder', '2023-11-12', 0, 0, 0),
	(43, '太', 'tài', 'trop', '2023-11-12', 0, 0, 0),
	(44, '红', 'hóng', 'rouge', '2023-11-12', 0, 0, 0),
	(45, '再见', 'zài jiàn', 'Au revoir', '2023-11-12', 0, 0, 0),
	(46, '对不起', 'Duìbùqǐ', 'Je suis désolé', '2023-11-12', 0, 0, 0),
	(47, '这里', 'Zhèlǐ', 'Ici', '2023-11-12', 0, 0, 0),
	(48, '厕所', 'Cèsuǒ', 'Toilettes', '2023-11-12', 0, 0, 0),
	(49, '没关系', 'Méiguānxì', 'Ce n’est pas grave (pas de relation)', '2023-11-12', 0, 0, 0);

INSERT INTO `version_words_count` (`id_test`, `test_date`, `words_count`) VALUES
	(1, '1991-12-03', 0);


INSERT INTO `theme_perf` (`id_test`, `test_date`, `test`) VALUES
	(1, '1991-12-03', 0);

INSERT INTO `theme_voc` (`id_word`, `zhongwen`, `pinyin`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
	(1, '汉语', 'Hàn yǔ', 'la langue chinoise', '2011-03-09', 14, 10, 71);

INSERT INTO `theme_words_count` (`id_test`, `test_date`, `words_count`) VALUES
	(1, '1991-12-03', 0);



/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
