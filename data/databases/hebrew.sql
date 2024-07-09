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
CREATE DATABASE wh0_Are_y0u_hebrew;
USE wh0_Are_y0u_hebrew;



-------------------------------------
--  T A B L E S   C R E A T I O N  --
-------------------------------------
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);


CREATE TABLE IF NOT EXISTS theme_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    `foreign` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `native` CHAR(255),
	creation_date DATE,
	nb TINYINT,
	score TINYINT,
	taux SMALLINT);


CREATE TABLE IF NOT EXISTS theme_words_count (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
	words_count SMALLINT);


CREATE TABLE IF NOT EXISTS version_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);


CREATE TABLE IF NOT EXISTS version_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    `foreign` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    `native` CHAR(255),
	creation_date DATE,
	nb TINYINT,
	score TINYINT,
	taux TINYINT);


CREATE TABLE IF NOT EXISTS version_words_count (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
	words_count SMALLINT
);

CREATE TABLE IF NOT EXISTS archive (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    hebrew VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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
INSERT INTO `version_voc` (`hebrew`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
    ('בהצלחה !', 'Bonne chance (bon succès !)', '2024-01-01', 0, 0, 0),
    ('בוקר', 'matin', '2024-01-01', 0, 0, 0),
    ('טוב', 'bon', '2024-01-01', 0, 0, 0),
    ('אור', 'lumière', '2024-01-01', 0, 0, 0),
    ('שיעור', 'leçon', '2024-01-01', 0, 0, 0),
    ('ראשון', 'premier', '2024-01-01', 0, 0, 0),
    ('בית', 'maison', '2024-01-01', 0, 0, 0),
    ('וו', 'crochet', '2024-01-01', 0, 0, 0),
    ('קוף', 'singe', '2024-01-01', 0, 0, 0),
    ('ראש', 'tête', '2024-01-01', 0, 0, 0),
    ('תרגיל', 'exercice', '2024-01-01', 0, 0, 0),
    ('לתרגם', 'traduire', '2024-01-01', 0, 0, 0),
    ('שלם', 'compléter', '2024-01-01', 0, 0, 0),
    ('עלות', 'montée', '2024-01-01', 0, 0, 0),
    ('שלום', 'bonjour / paix', '2024-01-01', 0, 0, 0),
    ('שני', 'deuxième (fém.)', '2024-01-01', 0, 0, 0),
    ('יד', 'main', '2024-01-01', 0, 0, 0),
    ('ללמוד', 'apprendre', '2024-01-01', 0, 0, 0),
    ('מים', 'eau', '2024-01-01', 0, 0, 0),
    ('שמיים', 'ciel', '2024-01-01', 0, 0, 0),
    ('שליש', 'troisième (fém.)', '2024-01-01', 0, 0, 0),
    ('מה', 'quoi', '2024-01-01', 0, 0, 0),
    ('טוב', 'bon, bien', '2024-01-01', 0, 0, 0),
    ('ככה ככה', 'comme-ci comme-ça', '2024-01-01', 0, 0, 0),
    ('כַּפִּ', 'cuillère', '2024-01-01', 0, 0, 0),
    ('תודה', 'merci', '2024-01-01', 0, 0, 0),
    ('רביעי', 'quatrième (fém.)', '2024-01-01', 0, 0, 0),
    ('אתה', 'toi (masc.)', '2024-01-01', 0, 0, 0),
    ('שותה', 'tu bois', '2024-01-01', 0, 0, 0),
    ('תה', 'thé', '2024-01-01', 0, 0, 0),
    ('בירה', 'bière', '2024-01-01', 0, 0, 0),
    ('את', 'toi (fém.)', '2024-01-01', 0, 0, 0),
    ('דלת', 'porte', '2024-01-01', 0, 0, 0),
    ('תו', 'signe / note de musique', '2024-01-01', 0, 0, 0),
    ('חמישי', 'cinquième (fém.)', '2024-01-01', 0, 0, 0),
    ('לומד', 'tu apprends (masc.)', '2024-01-01', 0, 0, 0),
    ('אני', 'moi', '2024-01-01', 0, 0, 0),
    ('לומדת', 'tu apprends (fém.)', '2024-01-01', 0, 0, 0),
    ('לטינית', 'le latin', '2024-01-01', 0, 0, 0),
    ('עין', 'œil, source', '2024-01-01', 0, 0, 0),
    ('עבר', 'passer, traverser (racine du mot hébreu)', '2024-01-01', 0, 0, 0),
    ('בסדר', 'd''accord', '2024-01-01', 0, 0, 0),
    ('חדש', 'neuf', '2024-01-01', 0, 0, 0),
    ('אין', 'Il n''y a pas', '2024-01-01', 0, 0, 0),
    ('חבל', 'dommage', '2024-01-01', 0, 0, 0),
    ('להתראות', 'au revoir', '2024-01-01', 0, 0, 0),
    ('חת', 'crainte', '2024-01-01', 0, 0, 0),
    ('סםכ', 'appuyer, soutenir', '2024-01-01', 0, 0, 0),
    ('חזרה', 'révision', '2024-01-01', 0, 0, 0),
    ('שמיני', 'huitième (fém.)', '2024-01-01', 0, 0, 0),
    ('דבורים', 'paroles', '2024-01-01', 0, 0, 0),
    ('מדבר', 'tu parles (masc.)', '2024-01-01', 0, 0, 0),
    ('לא', 'négation, pas', '2024-01-01', 0, 0, 0),
    ('רק', 'seulement', '2024-01-01', 0, 0, 0),
    ('של', 'de', '2024-01-01', 0, 0, 0),
    ('פה', 'bouche', '2024-01-01', 0, 0, 0),
    ('ורד', '(la) rose', '2024-01-01', 0, 0, 0),
    ('אידישׁ', 'yiddish', '2024-01-01', 0, 0, 0),
    ('אולפן', 'centre d''apprentissage de l''hébreu / studio de télévision', '2024-01-01', 0, 0, 0),
    ('המחשב', 'ordinateur', '2024-01-01', 0, 0, 0),
    ('תשיעי', 'la neuvième', '2024-01-01', 0, 0, 0),
    ('רוצה', 'vouloir', '2024-01-01', 0, 0, 0),
    ('אנחנו', 'nous', '2024-01-01', 0, 0, 0),
    ('לבן', 'pour le fils', '2024-01-01', 0, 0, 0),
    ('אינטרנט', 'internet', '2024-01-01', 0, 0, 0),
    ('והבת?', 'Et la fille ?', '2024-01-01', 0, 0, 0),
    ('מחשב נשׂא', 'ordinateur portable', '2024-01-01', 0, 0, 0),
    ('מחשוב', 'calculer / penser', '2024-01-01', 0, 0, 0),
    ('עשירי', 'dixième (la)', '2024-01-01', 0, 0, 0),
    ('ערב', 'soir', '2024-01-01', 0, 0, 0),
    ('אתן', 'vous (fém.)', '2024-01-01', 0, 0, 0),
    ('קפה', 'café', '2024-01-01', 0, 0, 0),
    ('עוגה', 'gâteau', '2024-01-01', 0, 0, 0),
    ('בבקשה', 's''il vous plaît (par demande)', '2024-01-01', 0, 0, 0),
    ('ישׂ', 'il y a ', '2024-01-01', 0, 0, 0),
    ('גבינה', 'fromage', '2024-01-01', 0, 0, 0),
    ('בקשה', 'demande', '2024-01-01', 0, 0, 0),
    ('גמאל', 'chameau', '2024-01-01', 0, 0, 0),
    ('שׁתה', 'boire', '2024-01-01', 0, 0, 0),
    ('חלב', 'lait', '2024-01-01', 0, 0, 0),
    ('או', 'ou', '2024-01-01', 0, 0, 0),
    ('סוכר', 'sucre', '2024-01-01', 0, 0, 0),
    ('מיץ', 'jus', '2024-01-01', 0, 0, 0),
    ('תפוז', 'orange', '2024-01-01', 0, 0, 0),
    ('תפוח', 'pomme', '2024-01-01', 0, 0, 0),
    ('זהב', 'or (métal précieux)', '2024-01-01', 0, 0, 0),
    ('נוס', 'miracle', '2024-01-01', 0, 0, 0),
    ('קניה', 'achat', '2024-01-01', 0, 0, 0),
    ('עייף', 'fatigué', '2024-01-01', 0, 0, 0),
    ('למה', 'pourquoi', '2024-01-01', 0, 0, 0),
    ('קניון', 'centre commercial', '2024-01-01', 0, 0, 0),
    ('אישה', 'femme', '2024-01-01', 0, 0, 0),
    ('פטפט', 'papotage', '2024-01-01', 0, 0, 0),
    ('איפה', 'où … ?', '2024-01-01', 0, 0, 0),
    ('החוט', 'le fil', '2024-01-01', 0, 0, 0),
    ('פאלפון', 'téléphone portable', '2024-01-01', 0, 0, 0),
    ('נד', 'qui bouge', '2024-01-01', 0, 0, 0),
    ('גם', 'aussi', '2024-01-01', 0, 0, 0),
    ('בעיה', 'problème', '2024-01-01', 0, 0, 0),
    ('מכונית', 'voiture', '2024-01-01', 0, 0, 0),
    ('פתוח', 'ouvrir', '2024-01-01', 0, 0, 0),
    ('קמץ', 'il a pincé', '2024-01-01', 0, 0, 0),
    ('סגול', 'ovale', '2024-01-01', 0, 0, 0),
    ('צרה', 'cassure', '2024-01-01', 0, 0, 0),
    ('קיבוץ', 'kibboutz', '2024-01-01', 0, 0, 0),
    ('ים', 'mer', '2024-01-01', 0, 0, 0),
    ('חוף', 'plage', '2024-01-01', 0, 0, 0),
    ('לשחות', 'nager', '2024-01-01', 0, 0, 0),
    ('חתיכה', 'morceau', '2024-01-01', 0, 0, 0),
    ('כנרת', 'Le lac de Tibériade', '2024-01-01', 0, 0, 0),
    ('כנור', 'cithare', '2024-01-01', 0, 0, 0),
    ('חדש', 'nouveau', '2024-01-01', 0, 0, 0),
    ('בקרוב', 'bientôt', '2024-01-01', 0, 0, 0),
    ('להבין', 'comprendre', '2024-01-01', 0, 0, 0),
    ('ל…', 'pour', '2024-01-01', 0, 0, 0),
    ('כי', 'parce que', '2024-01-01', 0, 0, 0),
    ('יפה', 'beau', '2024-01-01', 0, 0, 0),
    ('שמלה', 'robe', '2024-01-01', 0, 0, 0),
    ('מצוה', 'commandement', '2024-01-01', 0, 0, 0),
    ('תפילה', 'prière', '2024-01-01', 0, 0, 0),
    ('קדושׁ', 'bénédiction', '2024-01-01', 0, 0, 0),
    ('בלגן', 'désordre', '2024-01-01', 0, 0, 0),
    ('זה', 'ce', '2024-01-01', 0, 0, 0),
    ('פה', 'ici', '2024-01-01', 0, 0, 0),
    ('חדר', 'chambre', '2024-01-01', 0, 0, 0),
    ('מיטה', 'lit', '2024-01-01', 0, 0, 0),
    ('שׁם', 'là-bas', '2024-01-01', 0, 0, 0),
    ('שולחן', 'table', '2024-01-01', 0, 0, 0),
    ('כיסא', 'chaise', '2024-01-01', 0, 0, 0),
    ('אלה', 'ceux', '2024-01-01', 0, 0, 0),
    ('חתונת', 'mariage', '2024-01-01', 0, 0, 0),
    ('לאנ?', 'Vers où ?', '2024-01-01', 0, 0, 0),
    ('עם', 'avec', '2024-01-01', 0, 0, 0),
    ('מי', 'qui', '2024-01-01', 0, 0, 0),
    ('זאת', 'cette', '2024-01-01', 0, 0, 0),
    ('תל', 'colline', '2024-01-01', 0, 0, 0),
    ('אביב', 'printemps', '2024-01-01', 0, 0, 0),
    ('על', 'sur', '2024-01-01', 0, 0, 0),
    ('בעל', 'mari, possesseur, propriétaire / Baal', '2024-01-01', 0, 0, 0),
    ('משפחה', 'famille', '2024-01-01', 0, 0, 0),
    ('אבא', 'papa', '2024-01-01', 0, 0, 0),
    ('לשחק', 'jouer', '2024-01-01', 0, 0, 0),
    ('כדורגל', 'football', '2024-01-01', 0, 0, 0),
    ('כדור', 'balle', '2024-01-01', 0, 0, 0),
    ('רגל', 'pied', '2024-01-01', 0, 0, 0),
    ('אמא', 'maman', '2024-01-01', 0, 0, 0),
    ('אחיו', 'frère', '2024-01-01', 0, 0, 0),
    ('גדול', 'grand', '2024-01-01', 0, 0, 0),
    ('קטן', 'petit', '2024-01-01', 0, 0, 0),
    ('יד', 'main', '2024-01-01', 0, 0, 0),
    ('אחותו', 'sœur', '2024-01-01', 0, 0, 0),
    ('סל', 'panier', '2024-01-01', 0, 0, 0),
    ('סוף', 'fin', '2024-01-01', 0, 0, 0),
    ('שבוע', 'semaine', '2024-01-01', 0, 0, 0),
    ('סוף סוף', 'enfin', '2024-01-01', 0, 0, 0),
    ('ברכה', 'piscine', '2024-01-01', 0, 0, 0),
    ('ללכת', 'aller', '2024-01-01', 0, 0, 0),
    ('חבר', 'ami', '2024-01-01', 0, 0, 0),
    ('לאכול', 'manger', '2024-01-01', 0, 0, 0),
    ('אש', 'feu', '2024-01-01', 0, 0, 0),
    ('על האשׁ', 'au barbecue', '2024-01-01', 0, 0, 0),
    ('בכפ', 'avec plaisir', '2024-01-01', 0, 0, 0),
    ('דואר', 'courrier', '2024-01-01', 0, 0, 0),
    ('אולי', 'peut-être', '2024-01-01', 0, 0, 0),
    ('כוח', 'pouvoir', '2024-01-01', 0, 0, 0),
    ('לעזור', 'aider', '2024-01-01', 0, 0, 0),
    ('כתובת', 'adresse', '2024-01-01', 0, 0, 0),
    ('כהנ', 'Cohen', '2024-01-01', 0, 0, 0),
    ('תודה לך', 'merci à toi', '2024-01-01', 0, 0, 0),
    ('כן', 'oui', '2024-01-01', 0, 0, 0),
    ('שׁטרודל', 'arobase', '2024-01-01', 0, 0, 0),
    ('נקודה', 'point', '2024-01-01', 0, 0, 0),
    ('שדה תעופה', 'aéroport', '2024-01-01', 0, 0, 0),
    ('שדה', 'champ', '2024-01-01', 0, 0, 0),
    ('סליחה', 'pardon', '2024-01-01', 0, 0, 0),
    ('טיסה', 'vol d''avion', '2024-01-01', 0, 0, 0),
    ('ראה', 'voir', '2024-01-01', 0, 0, 0),
    ('מזוודה', 'valise', '2024-01-01', 0, 0, 0),
    ('כמה', 'combien', '2024-01-01', 0, 0, 0),
    ('רק', 'seulement', '2024-01-01', 0, 0, 0),
    ('תעופה', 'aviation', '2024-01-01', 0, 0, 0),
    ('בן אדם', 'homme, être humain (fils d''Adam)', '2024-01-01', 0, 0, 0),
    ('מאוד', 'très', '2024-01-01', 0, 0, 0),
    ('תמונה', 'photo', '2024-01-01', 0, 0, 0),
    ('זמנה', 'invitation', '2024-01-01', 0, 0, 0),
    ('מתי …?', 'quand … ?', '2024-01-01', 0, 0, 0),
    ('ארוחה', 'repas', '2024-01-01', 0, 0, 0),
    ('אפשר', 'possible', '2024-01-01', 0, 0, 0),
    ('איאפשר', 'impossible', '2024-01-01', 0, 0, 0),
    ('יום ראשון', 'dimanche', '2024-01-01', 0, 0, 0),
    ('זמן', 'temps', '2024-01-01', 0, 0, 0),
    ('עובד', 'travailler', '2024-01-01', 0, 0, 0),
    ('אז', 'alors', '2024-01-01', 0, 0, 0),
    ('צלום', 'image', '2024-01-01', 0, 0, 0),
    ('צריך', 'avoir besoin de', '2024-01-01', 0, 0, 0),
    ('חנות', 'magasin', '2024-01-01', 0, 0, 0),
    ('נמוך', 'bas', '2024-01-01', 0, 0, 0),
    ('העליון', 'haut', '2024-01-01', 0, 0, 0),
    ('מהר', 'vite', '2024-01-01', 0, 0, 0),
    ('מצלמה', 'appareil photo', '2024-01-01', 0, 0, 0),
    ('חובב', 'amateur', '2024-01-01', 0, 0, 0),
    ('ילד', 'enfant', '2024-01-01', 0, 0, 0),
    ('מצוינת', 'excellent', '2024-01-01', 0, 0, 0),
    ('הארץ', 'le pays / Israël', '2024-01-01', 0, 0, 0),
    ('דרכון', 'passeport', '2024-01-01', 0, 0, 0),
    ('ימאי', 'marin (dérivé de "eau")', '2024-01-01', 0, 0, 0),
    ('דרכ', 'chemin', '2024-01-01', 0, 0, 0),
    ('שׁבתון', 'congé', '2024-01-01', 0, 0, 0),
    ('עד', 'jusqu''à', '2024-01-01', 0, 0, 0),
    ('בן כמה אתה', 'Quel âge as-tu ?', '2024-01-01', 0, 0, 0),
    ('צבא', 'armée', '2024-01-01', 0, 0, 0),
    ('לפני', 'avant', '2024-01-01', 0, 0, 0),
    ('אחר', 'après', '2024-01-01', 0, 0, 0),
    ('מכתב', 'lettre (courrier)', '2024-01-01', 0, 0, 0),
    ('כבר', 'déjà', '2024-01-01', 0, 0, 0),
    ('חם', 'chaud', '2024-01-01', 0, 0, 0),
    ('לילה', 'nuit', '2024-01-01', 0, 0, 0),
    ('מפני שׁ…', 'parce que', '2024-01-01', 0, 0, 0),
    ('כל היום', 'toute la journée', '2024-01-01', 0, 0, 0),
    ('כל יום', 'tous les jours', '2024-01-01', 0, 0, 0),
    ('בגלל', 'à cause de', '2024-01-01', 0, 0, 0),
    ('אדום', 'rouge', '2024-01-01', 0, 0, 0),
    ('שם', 'là-bas, là-haut', '2024-01-01', 0, 0, 0),
    ('רב', 'beaucoup', '2024-01-01', 0, 0, 0),
    ('שמים', 'cieux', '2024-01-01', 0, 0, 0),
    ('נכנס יין יצא סוד', 'le vin entre, le secret sort', '2024-01-01', 0, 0, 0),
    ('ליפול', 'tomber', '2024-01-01', 0, 0, 0),
    ('רגל', 'jambe', '2024-01-01', 0, 0, 0),
    ('מה קרה?', 'Que s''est-il passé ?', '2024-01-01', 0, 0, 0),
    ('חודש', 'mois', '2024-01-01', 0, 0, 0),
    ('גבעה', 'colline', '2024-01-01', 0, 0, 0),
    ('תמר', 'datte, dattier', '2024-01-01', 0, 0, 0),
    ('ורד', 'rose, rosier', '2024-01-01', 0, 0, 0),
    ('אורן', 'pin', '2024-01-01', 0, 0, 0),
    ('צעיר', 'jeune', '2024-01-01', 0, 0, 0),
    ('סבא', 'grand-père', '2024-01-01', 0, 0, 0),
    ('להיוולד', 'naître', '2024-01-01', 0, 0, 0),
    ('נכד', 'petit-fils', '2024-01-01', 0, 0, 0),
    ('לפני שבוע', 'la semaine dernière', '2024-01-01', 0, 0, 0),
    ('ברית', 'alliance', '2024-01-01', 0, 0, 0),
    ('גיל', 'âge', '2024-01-01', 0, 0, 0),
    ('באותו', 'même', '2024-01-01', 0, 0, 0),
    ('כאשר', 'Quand …, ... .', '2024-01-01', 0, 0, 0),
    ('מילה', 'coupure', '2024-01-01', 0, 0, 0),
    ('קולנוע', 'cinéma', '2024-01-01', 0, 0, 0),
    ('קול', 'voix', '2024-01-01', 0, 0, 0),
    ('נוע', 'mouvement', '2024-01-01', 0, 0, 0),
    ('אתמול', 'hier', '2024-01-01', 0, 0, 0),
    ('כמו', 'comme', '2024-01-01', 0, 0, 0),
    ('שוב', 'de nouveau', '2024-01-01', 0, 0, 0),
    ('לשבור', 'briser', '2024-01-01', 0, 0, 0),
    ('אופן', 'roue', '2024-01-01', 0, 0, 0),
    ('חלל', 'espace (cosmique)', '2024-01-01', 0, 0, 0),
    ('ללוות', 'accompagner', '2024-01-01', 0, 0, 0),
    ('מתנה', 'cadeau', '2024-01-01', 0, 0, 0),
    ('להזמין', 'inviter', '2024-01-01', 0, 0, 0),
    ('יום הולדת', 'jour de naissance', '2024-01-01', 0, 0, 0),
    ('עוד לא', 'pas encore', '2024-01-01', 0, 0, 0),
    ('לחשוב', 'penser', '2024-01-01', 0, 0, 0),
    ('הטוב ביותר', 'le meilleur', '2024-01-01', 0, 0, 0),
    ('כסף', 'argent', '2024-01-01', 0, 0, 0),
    ('במזומן', 'en liquide', '2024-01-01', 0, 0, 0),
    ('איזה', 'Quel … !', '2024-01-01', 0, 0, 0),
    ('שביתה', 'grève', '2024-01-01', 0, 0, 0),
    ('השעה', 'l''heure', '2024-01-01', 0, 0, 0),
    ('מישהו', 'quelqu''un', '2024-01-01', 0, 0, 0),
    ('מחר', 'demain', '2024-01-01', 0, 0, 0),
    ('כבוד', 'honneur', '2024-01-01', 0, 0, 0),
    ('סיבה', 'raison', '2024-01-01', 0, 0, 0),
    ('נישואים', 'mariage', '2024-01-01', 0, 0, 0),
    ('חם', 'chaud / beau-père', '2024-01-01', 0, 0, 0),
    ('חםות', 'chaudes / belle-mère', '2024-01-01', 0, 0, 0),
    ('נעים', 'agréable', '2024-01-01', 0, 0, 0),
    ('ממשׁ', 'réellement', '2024-01-01', 0, 0, 0),
    ('תמיד', 'toujours', '2024-01-01', 0, 0, 0),
    ('ביחס', 'relation', '2024-01-01', 0, 0, 0);


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
