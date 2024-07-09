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
CREATE DATABASE wh0_Are_y0u_russian;
USE wh0_Are_y0u_russian;



-------------------------------------
--  T A B L E S   C R E A T I O N  --
-------------------------------------
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT
);

CREATE TABLE IF NOT EXISTS theme_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    `foreign` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `native` CHAR(255),
	creation_date DATE,
	nb TINYINT,
	score TINYINT,
	taux SMALLINT
);

CREATE TABLE IF NOT EXISTS theme_words_count (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
	words_count SMALLINT
);

CREATE TABLE IF NOT EXISTS version_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT
);

CREATE TABLE IF NOT EXISTS version_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    `foreign` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `native` CHAR(255),
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

CREATE TABLE IF NOT EXISTS archive (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    russian VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255)
);



------------------------------------------
--  T A B L E S   P E R M I S S I O N S --
------------------------------------------
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
INSERT INTO `version_voc` (`russian`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
	('адрес', 'adresse', '2024-01-01', 0, 0, 0),
	('паспорт', 'passeport', '2024-01-01', 0, 0, 0),
	('кредит', 'crédit', '2024-01-01', 0, 0, 0),
	('гараж', 'garage', '2024-01-01', 0, 0, 0),
	('кофе', 'café', '2024-01-01', 0, 0, 0),
	('бар', 'bar', '2024-01-01', 0, 0, 0),
	('чек', 'chèque', '2024-01-01', 0, 0, 0),
	('ключ', 'clé', '2024-01-01', 0, 0, 0),
	('шофер', 'chauffeur', '2024-01-01', 0, 0, 0),
	('телефон', 'téléphone', '2024-01-01', 0, 0, 0),
	('медицина', 'médecine', '2024-01-01', 0, 0, 0),
	('консул', 'consul', '2024-01-01', 0, 0, 0),
	('почта', 'poste', '2024-01-01', 0, 0, 0),
	('минут', 'minute', '2024-01-01', 0, 0, 0),
	('багаж', 'bagage', '2024-01-01', 0, 0, 0),
	('вагон', 'wagon', '2024-01-01', 0, 0, 0),
	('газ', 'gaz', '2024-01-01', 0, 0, 0),
	('костюм', 'costume', '2024-01-01', 0, 0, 0),
	('газета', 'journal', '2024-01-01', 0, 0, 0),
	('пианист', 'pianiste', '2024-01-01', 0, 0, 0),
	('акцент', 'accent', '2024-01-01', 0, 0, 0),
	('инженер', 'ingénieur', '2024-01-01', 0, 0, 0),
	('один', 'un (nombre)', '2024-01-01', 0, 0, 0),
	('первый', 'première', '2024-01-01', 0, 0, 0),
	('как', 'comment', '2024-01-01', 0, 0, 0),
	('добрый ', 'bon', '2024-01-01', 0, 0, 0),
	('хорошо', 'bien, d''accord, très bien', '2024-01-01', 0, 0, 0),
	('куда', 'vers où ?', '2024-01-01', 0, 0, 0),
	('дела', 'affaires', '2024-01-01', 0, 0, 0),
	('идти', 'aller', '2024-01-01', 0, 0, 0),
	('день', 'jour', '2024-01-01', 0, 0, 0),
	('a', 'et / aussi', '2024-01-01', 0, 0, 0),
	('большой', 'grand', '2024-01-01', 0, 0, 0),
	('какой', 'lequel', '2024-01-01', 0, 0, 0),
	('до', 'jusqu''à', '2024-01-01', 0, 0, 0),
	('свидания', 'rendez-vous (amoureux) / rencontre', '2024-01-01', 0, 0, 0),
	('дом', 'maison', '2024-01-01', 0, 0, 0),
	('упражнения', 'exercices', '2024-01-01', 0, 0, 0),
	('Читайте', 'lisez', '2024-01-01', 0, 0, 0),
	('Переводите', 'traduisez', '2024-01-01', 0, 0, 0),
	('восстановите', 'reconstituez', '2024-01-01', 0, 0, 0),
	('текст', 'texte', '2024-01-01', 0, 0, 0),
	('одиннадцать', 11, '2024-01-01', 0, 0, 0),
	('второй', 'deuxième', '2024-01-01', 0, 0, 0),
	('рад', 'content', '2024-01-01', 0, 0, 0),
	('кто', 'qui', '2024-01-01', 0, 0, 0),
	('говорить', 'parler', '2024-01-01', 0, 0, 0),
	('Здравствуй', 'Bonjour (tutoiement)', '2024-01-01', 0, 0, 0),
	('Здравствуйте', 'Bonjour (vouvoiement)', '2024-01-01', 0, 0, 0),
	('друг', 'ami', '2024-01-01', 0, 0, 0),
	('Бог', 'Dieu', '2024-01-01', 0, 0, 0),
	('и', 'et / aussi', '2024-01-01', 0, 0, 0),
	('я', 'je', '2024-01-01', 0, 0, 0),
	('ты', 'tu', '2024-01-01', 0, 0, 0),
	('это', 'il', '2024-01-01', 0, 0, 0),
	('она', 'elle', '2024-01-01', 0, 0, 0),
	('мы', 'nous', '2024-01-01', 0, 0, 0),
	('вы', 'vous', '2024-01-01', 0, 0, 0),
	('они', 'ils, elles', '2024-01-01', 0, 0, 0),
	('тоже', 'aussi', '2024-01-01', 0, 0, 0),
	('где', 'où', '2024-01-01', 0, 0, 0),
	('театр', 'théâtre', '2024-01-01', 0, 0, 0),
	('приходи', 'passe (me voir)', '2024-01-01', 0, 0, 0),
	('встречи', 'rencontre', '2024-01-01', 0, 0, 0),
	('до встречи ', 'à la prochaine', '2024-01-01', 0, 0, 0),
	('третий', 'troisième', '2024-01-01', 0, 0, 0),
	('извините / простите', 'excusez-moi', '2024-01-01', 0, 0, 0),
	('спасибо', 'merci', '2024-01-01', 0, 0, 0),
	('очень', 'très', '2024-01-01', 0, 0, 0),
	('любезный', 'aimable', '2024-01-01', 0, 0, 0),
	('конечно', 'bien sûr, il est certain', '2024-01-01', 0, 0, 0),
	('давать', 'donner, offrir / accorder', '2024-01-01', 0, 0, 0),
	('Давайте работать!', 'Travaillons !', '2024-01-01', 0, 0, 0),
	('с удовольствием', 'avec plaisir', '2024-01-01', 0, 0, 0),
	('язык', 'langage', '2024-01-01', 0, 0, 0),
	('француз', 'Français', '2024-01-01', 0, 0, 0),
	('немец', 'Allemand', '2024-01-01', 0, 0, 0),
	('Спаси вас Бог', 'Que Dieu vous garde', '2024-01-01', 0, 0, 0),
	('четвертый', 'quatrième', '2024-01-01', 0, 0, 0),
	('всë', 'tout', '2024-01-01', 0, 0, 0),
	('понимаю', 'je comprends', '2024-01-01', 0, 0, 0),
	('делаешь', 'tu fais', '2024-01-01', 0, 0, 0),
	('учу', 'j''apprend', '2024-01-01', 0, 0, 0),
	('немного', 'un peu', '2024-01-01', 0, 0, 0),
	('но', 'mais', '2024-01-01', 0, 0, 0),
	('знаешь', 'tu connais', '2024-01-01', 0, 0, 0),
	('Пока!', 'Salut ! A plus !', '2024-01-01', 0, 0, 0),
	('Как …. по-русски?', 'Comment dit-on … en russe ?', '2024-01-01', 0, 0, 0),
	('правда', True, '2024-01-01', 0, 0, 0),
	('значить', 'signifier', '2024-01-01', 0, 0, 0),
	('значит', 'Ça veut dire que / donc', '2024-01-01', 0, 0, 0),
	('ясно', 'clair', '2024-01-01', 0, 0, 0),
	('уже', 'déjà', '2024-01-01', 0, 0, 0),
	('к сожалению', 'malheureusement', '2024-01-01', 0, 0, 0),
	('девушка', 'jeune fille', '2024-01-01', 0, 0, 0),
	('подруга', 'amie', '2024-01-01', 0, 0, 0),
	('пятый', 'cinquième', '2024-01-01', 0, 0, 0),
	('-cя', 'suffixe d''un verbe à la forme pronominale', '2024-01-01', 0, 0, 0),
	('с удовольствием!', 'avec plaisir !', '2024-01-01', 0, 0, 0),
	('пoзнакомиться', 'faire connaissance', '2024-01-01', 0, 0, 0),
	('меня', 'moi (accusatif)', '2024-01-01', 0, 0, 0),
	('звать', 's''appeler', '2024-01-01', 0, 0, 0),
	('вac', 'vous (accusatif)', '2024-01-01', 0, 0, 0),
	('приятный', 'agréable', '2024-01-01', 0, 0, 0),
	('имя', 'prénom', '2024-01-01', 0, 0, 0),
	('кстати', 'à propos', '2024-01-01', 0, 0, 0),
	('его', 'lui (accusatif)', '2024-01-01', 0, 0, 0),
	('известный', 'célèbre', '2024-01-01', 0, 0, 0),
	('вот', 'voici', '2024-01-01', 0, 0, 0),
	('eë', 'elle (accusatif)', '2024-01-01', 0, 0, 0),
	('шестой', 'sixième', '2024-01-01', 0, 0, 0),
	('жить', 'vivre', '2024-01-01', 0, 0, 0),
	('скажите, …', 'dites, …', '2024-01-01', 0, 0, 0),
	('pаботать', 'travailler', '2024-01-01', 0, 0, 0),
	('актер', 'acteur', '2024-01-01', 0, 0, 0),
	('режиссер', 'régisseur', '2024-01-01', 0, 0, 0),
	('интересный', 'intéressant', '2024-01-01', 0, 0, 0),
	('город', 'ville', '2024-01-01', 0, 0, 0),
	('кто он', 'Que fait-il dans la vie ?', '2024-01-01', 0, 0, 0),
	('Москва', 'Moscou', '2024-01-01', 0, 0, 0),
	('Киев', 'Kiev', '2024-01-01', 0, 0, 0),
	('журналистка', 'journaliste', '2024-01-01', 0, 0, 0),
	('ваш', 'votre (pour un homme)', '2024-01-01', 0, 0, 0),
	('ваша', 'votre (pour une femme)', '2024-01-01', 0, 0, 0),
	('журнал', 'revue', '2024-01-01', 0, 0, 0),
	('его', 'sa', '2024-01-01', 0, 0, 0),
	('экзамен', 'examen', '2024-01-01', 0, 0, 0),
	('спрашивать', 'interroger', '2024-01-01', 0, 0, 0),
	('живëте', 'vous vivez', '2024-01-01', 0, 0, 0),
	('вижу', 'je vois', '2024-01-01', 0, 0, 0),
	('живëт', 'il vit', '2024-01-01', 0, 0, 0),
	('седмой', 'septième', '2024-01-01', 0, 0, 0),
	('тридцать', 'trente', '2024-01-01', 0, 0, 0),
	('знаем', 'nous connaissons', '2024-01-01', 0, 0, 0),
	('Вы нас знаете', 'Vous nous connaissez', '2024-01-01', 0, 0, 0),
	('Она их понимает', 'Elle les comprends', '2024-01-01', 0, 0, 0),
	('быть', 'être', '2024-01-01', 0, 0, 0),
	('приглашаю', 'j''invite', '2024-01-01', 0, 0, 0),
	('восьмой', 'huitième', '2024-01-01', 0, 0, 0),
	('прeкрасная', 'jolie, belle', '2024-01-01', 0, 0, 0),
	('семья', 'famille', '2024-01-01', 0, 0, 0),
	('же', 'donc', '2024-01-01', 0, 0, 0),
	('молодая', 'jeune (féminin)', '2024-01-01', 0, 0, 0),
	('женщина', 'femme', '2024-01-01', 0, 0, 0),
	('так', 'ainsi', '2024-01-01', 0, 0, 0),
	('говорят', 'on dit (ils disent)', '2024-01-01', 0, 0, 0),
	('лицо', 'visage', '2024-01-01', 0, 0, 0),
	('сын', 'fils', '2024-01-01', 0, 0, 0),
	('дочь', 'fille', '2024-01-01', 0, 0, 0),
	('дети', 'enfants', '2024-01-01', 0, 0, 0),
	('фигура', 'silhouette', '2024-01-01', 0, 0, 0),
	('за', 'pour', '2024-01-01', 0, 0, 0),
	('отец', 'père', '2024-01-01', 0, 0, 0),
	('мужчина', 'homme', '2024-01-01', 0, 0, 0),
	('интересный', 'beau', '2024-01-01', 0, 0, 0),
	('У вас есть … ?', 'Est-ce que vous avez … ?', '2024-01-01', 0, 0, 0),
	('замужнeм', 'mariée', '2024-01-01', 0, 0, 0),
	('женат', 'marié', '2024-01-01', 0, 0, 0),
	('они женаты', 'ils sont mariés', '2024-01-01', 0, 0, 0),
	('чудесный', 'merveilleux', '2024-01-01', 0, 0, 0),
	('муж', 'mari', '2024-01-01', 0, 0, 0),
	('мать', 'mère', '2024-01-01', 0, 0, 0),
	('словарь', 'dictionnaire', '2024-01-01', 0, 0, 0),
	('повторение', 'répétition', '2024-01-01', 0, 0, 0),
	('девятый', 'neuvième', '2024-01-01', 0, 0, 0),
	('сорок', 'quarante', '2024-01-01', 0, 0, 0),
	('жениться', 'se marier', '2024-01-01', 0, 0, 0),
	('сюрприз', 'surprise', '2024-01-01', 0, 0, 0),
	('Попробуй!', 'Essaie !', '2024-01-01', 0, 0, 0),
	('попробовать', 'essayer', '2024-01-01', 0, 0, 0),
	('угадать', 'deviner', '2024-01-01', 0, 0, 0),
	('думаю', 'je pense', '2024-01-01', 0, 0, 0),
	('легко / ленко', 'facile', '2024-01-01', 0, 0, 0),
	('хотеть', 'vouloir', '2024-01-01', 0, 0, 0),
	('умный', 'intelligent', '2024-01-01', 0, 0, 0),
	('она такая умная!', 'Elle est si intelligente !', '2024-01-01', 0, 0, 0),
	('почему', 'pourquoi', '2024-01-01', 0, 0, 0),
	('сказать', 'dire', '2024-01-01', 0, 0, 0),
	('невеста', 'fiancée', '2024-01-01', 0, 0, 0),
	('десятый', 'dixième', '2024-01-01', 0, 0, 0),
	('молодец', 'débrouillard', '2024-01-01', 0, 0, 0),
	('рад тибя услышать', 'content de t''entendre', '2024-01-01', 0, 0, 0),
	('ты были', 'tu étais', '2024-01-01', 0, 0, 0),
	('утром', 'le matin', '2024-01-01', 0, 0, 0),
	('звить', 'téléphoner', '2024-01-01', 0, 0, 0),
	('днëм', 'après-midi', '2024-01-01', 0, 0, 0),
	('увы', 'hélas', '2024-01-01', 0, 0, 0),
	('потом', 'après', '2024-01-01', 0, 0, 0),
	('стыно', 'honte', '2024-01-01', 0, 0, 0),
	('каникулы', 'vacances scolaires', '2024-01-01', 0, 0, 0),
	('пятьдесят', 'cinquante', '2024-01-01', 0, 0, 0),
	('лишний', 'superflu', '2024-01-01', 0, 0, 0),
	('гулять', 'se promener', '2024-01-01', 0, 0, 0),
	('роза', 'la rose (fleur)', '2024-01-01', 0, 0, 0),
	('понятно', '(c''est) compris', '2024-01-01', 0, 0, 0),
	('пожалуйста', 's''il vous plaît', '2024-01-01', 0, 0, 0),
	('желание', 'souhait', '2024-01-01', 0, 0, 0),
	('Я должен', 'je dois', '2024-01-01', 0, 0, 0),
	('извинить', 'excuser', '2024-01-01', 0, 0, 0),
	('Tы всë понятно ?', 'Tu as tout compris ?', '2024-01-01', 0, 0, 0),
	('может', 'peut-être', '2024-01-01', 0, 0, 0),
	('пойдëм', 'nous irons', '2024-01-01', 0, 0, 0),
	('здесь', 'ici', '2024-01-01', 0, 0, 0),
	('всегда', 'toujours', '2024-01-01', 0, 0, 0),
	('если', 'si (condition)', '2024-01-01', 0, 0, 0),
	('шестьдесят', 'soixantième', '2024-01-01', 0, 0, 0),
	('весь', 'tout (nominatif)', '2024-01-01', 0, 0, 0),
	('Я буду работать', 'Je travaillerai', '2024-01-01', 0, 0, 0),
	('писать', 'écrire', '2024-01-01', 0, 0, 0),
	('вы сами', 'vous-mêmes', '2024-01-01', 0, 0, 0),
	('тринадцатый', 'treizième', '2024-01-01', 0, 0, 0),
	('ехать', '-> fahren', '2024-01-01', 0, 0, 0),
	('нами', 'nous (instrumental)', '2024-01-01', 0, 0, 0),
	('когда', 'quand', '2024-01-01', 0, 0, 0),
	('Мне нeкогда', 'je n''ai pas le temps', '2024-01-01', 0, 0, 0),
	('там', 'là-bas', '2024-01-01', 0, 0, 0),
	('без', 'sans', '2024-01-01', 0, 0, 0),
	('труд', 'travail, peine, œuvre', '2024-01-01', 0, 0, 0),
	('вынуть', 'retirer', '2024-01-01', 0, 0, 0),
	('рыба', 'poisson', '2024-01-01', 0, 0, 0),
	('из', 'hors de', '2024-01-01', 0, 0, 0),
	('пруд', 'étang', '2024-01-01', 0, 0, 0),
	('Успехов тeбe', 'Bonne chance à toi !', '2024-01-01', 0, 0, 0),
	('успех', 'succès', '2024-01-01', 0, 0, 0),
	('семьдесят', 'soixante-dix', '2024-01-01', 0, 0, 0),
	('четырнадцатый', 'quatorzième', '2024-01-01', 0, 0, 0),
	('дедушка', 'grand-père', '2024-01-01', 0, 0, 0),
	('бабушка', 'grand-mère', '2024-01-01', 0, 0, 0),
	('книга', 'livre', '2024-01-01', 0, 0, 0),
	('твой', 'le tien', '2024-01-01', 0, 0, 0),
	('нашa', 'notre / le nôtre', '2024-01-01', 0, 0, 0),
	('вашe', 'votre / le vôtre', '2024-01-01', 0, 0, 0),
	('его', 'son / le sien (pour un homme)', '2024-01-01', 0, 0, 0),
	('eë', 'son / le sien (pour une femme)', '2024-01-01', 0, 0, 0),
	('китайский', 'chinois (adjectif)', '2024-01-01', 0, 0, 0),
	('китаец', 'chinois (nom)', '2024-01-01', 0, 0, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
