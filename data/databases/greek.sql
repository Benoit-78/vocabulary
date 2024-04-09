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
CREATE DATABASE wh0_Are_y0u_greek;
USE wh0_Are_y0u_greek;



-------------------------------------
--  T A B L E S   C R E A T I O N  --
-------------------------------------
CREATE TABLE IF NOT EXISTS theme_perf (
	id_test SMALLINT AUTO_INCREMENT PRIMARY KEY,
    test_date DATE,
    test TINYINT);


CREATE TABLE IF NOT EXISTS theme_voc (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    greek CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255),
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
    greek CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255),
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
    greek CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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
INSERT INTO `version_voc` (`greek`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
    ('τρεχειν', 'courir', '2024-01-01', 0, 0, 0),
    ('πρωτον', 'premièrement', '2024-01-01', 0, 0, 0),
    ('παρα', 'auprès de', '2024-01-01', 0, 0, 0),
    ('το ελαιον', 'l''huile', '2024-01-01', 0, 0, 0),
    ('ο αηρ', 'l''air', '2024-01-01', 0, 0, 0),
    ('εχω', 'dehors', '2024-01-01', 0, 0, 0),
    ('ο ετερος', 'l''autre', '2024-01-01', 0, 0, 0),
    ('ο παις', 'l''enfant', '2024-01-01', 0, 0, 0),
    ('γραφειν', 'écrire', '2024-01-01', 0, 0, 0),
    ('ταδε', 'ceci', '2024-01-01', 0, 0, 0),
    ('ευ', 'bien, bon', '2024-01-01', 0, 0, 0),
    ('η θαλαττα', 'la mer', '2024-01-01', 0, 0, 0),
    ('το γραμμα', 'la lettre', '2024-01-01', 0, 0, 0),
    ('ακουω', 'écouter', '2024-01-01', 0, 0, 0),
    ('μανθανει', 'apprendre', '2024-01-01', 0, 0, 0),
    ('ματημα', 'la leçon', '2024-01-01', 0, 0, 0),
    ('η απορια', 'l''embarras', '2024-01-01', 0, 0, 0),
    ('μονον', 'seulement', '2024-01-01', 0, 0, 0),
    ('γυμναζειν', 'l''entraînement physique', '2024-01-01', 0, 0, 0),
    ('το σωμα', 'le corps', '2024-01-01', 0, 0, 0),
    ('το τοπος', 'le lieu', '2024-01-01', 0, 0, 0),
    ('παντες', 'tous', '2024-01-01', 0, 0, 0),
    ('καλεω', 'appeler, nommer', '2024-01-01', 0, 0, 0),
    ('ο δρομος', 'la course', '2024-01-01', 0, 0, 0),
    ('ασκειν', 's''exercer', '2024-01-01', 0, 0, 0),
    ('ο καλος', 'le beau', '2024-01-01', 0, 0, 0),
    ('ο αγαθος', 'le bon', '2024-01-01', 0, 0, 0),
    ('γυμνος', 'nu', '2024-01-01', 0, 0, 0),
    ('πραττει', 'agir', '2024-01-01', 0, 0, 0),
    ('η χειρ', 'la main', '2024-01-01', 0, 0, 0),
    ('κατα', 'de haut en bas', '2024-01-01', 0, 0, 0),
    ('το εργον', 'le travail', '2024-01-01', 0, 0, 0),
    ('η γη', 'la terr', '2024-01-01', 0, 0, 0),
    ('ολιγον', 'un peu', '2024-01-01', 0, 0, 0),
    ('τριβειν', 'frotter, user', '2024-01-01', 0, 0, 0),
    ('η θυρα', 'la porte', '2024-01-01', 0, 0, 0),
    ('κοινον', 'commun', '2024-01-01', 0, 0, 0),
    ('μετα', 'avec', '2024-01-01', 0, 0, 0),
    ('περι', 'au sujet de', '2024-01-01', 0, 0, 0),
    ('φοβουμαι', 'je redoute', '2024-01-01', 0, 0, 0),
    ('πολυ', 'beaucoup', '2024-01-01', 0, 0, 0),
    ('πλείω', 'davantage', '2024-01-01', 0, 0, 0),
    ('τὸ πραγμα', 'la chose, l''affaire', '2024-01-01', 0, 0, 0),
    ('τὸ ὕδωρ', 'l''eau', '2024-01-01', 0, 0, 0),
    ('ὁ χένος', 'l''étranger', '2024-01-01', 0, 0, 0),
    ('ὁ πατήρ', 'le père', '2024-01-01', 0, 0, 0),
    ('ὁ γάμος', 'le mariage', '2024-01-01', 0, 0, 0),
    ('ὁ τράχηλος', 'le cou', '2024-01-01', 0, 0, 0),
    ('ἀγγέλλω', 'j''annonce', '2024-01-01', 0, 0, 0),
    ('ὁ ἅγιος', 'le saint', '2024-01-01', 0, 0, 0),
    ('ὁ ἀργός', 'le champ', '2024-01-01', 0, 0, 0),
    ('τὸ ἁίμα', 'le sang', '2024-01-01', 0, 0, 0),
    ('τὸ ἄλγος', 'la douleur', '2024-01-01', 0, 0, 0),
    ('ἀλητής', 'véritable', '2024-01-01', 0, 0, 0),
    ('ἀμύνω', 'défendre', '2024-01-01', 0, 0, 0),
    ('ὁ ἄνεμος', 'le vent', '2024-01-01', 0, 0, 0),
    ('ἀπιθμέω', 'je compte', '2024-01-01', 0, 0, 0),
    ('ἄριστος', 'le meilleur', '2024-01-01', 0, 0, 0),
    ('ἡ ἀρχή', 'le début', '2024-01-01', 0, 0, 0),
    ('τό ἄσθμα', 'l''essouflement', '2024-01-01', 0, 0, 0),
    ('τὸ βαλανεϊον', 'le bain', '2024-01-01', 0, 0, 0),
    ('ὁ βασιλεύς', 'le roi', '2024-01-01', 0, 0, 0),
    ('τό βιβλίον', 'le livre', '2024-01-01', 0, 0, 0),
    ('ὁ βίος', 'la vie', '2024-01-01', 0, 0, 0),
    ('ὁ βους', 'la vache, le bœuf', '2024-01-01', 0, 0, 0),
    ('τὸ γαλα', 'le lait', '2024-01-01', 0, 0, 0),
    ('ἡ γαστήρ', 'le ventre', '2024-01-01', 0, 0, 0),
    ('ἡ γένεσις', 'l''origine, la création', '2024-01-01', 0, 0, 0),
    ('τό γένος', 'la famille, la race', '2024-01-01', 0, 0, 0),
    ('ἡ γλωττα', 'la langue', '2024-01-01', 0, 0, 0),
    ('ἡ γυνή', 'la femme', '2024-01-01', 0, 0, 0),
    ('ἡ γωνία', 'le coin, l''angle', '2024-01-01', 0, 0, 0),
    ('ὁ δαίμων', 'la divinité', '2024-01-01', 0, 0, 0),
    ('ἡ δάφνη', 'le laurir', '2024-01-01', 0, 0, 0),
    ('τό δένδρον', 'l''arbre', '2024-01-01', 0, 0, 0),
    ('ὁ δεσπότης', 'le maître de maison', '2024-01-01', 0, 0, 0),
    ('ὁ δημος', 'le peuple', '2024-01-01', 0, 0, 0),
    ('διδάσκω', 'j''enseigne', '2024-01-01', 0, 0, 0),
    ('τό ἔθνος', 'le peuple, la nation', '2024-01-01', 0, 0, 0),
    ('ὁ εἰκών', 'l''image', '2024-01-01', 0, 0, 0),
    ('ἡ εἰρήνη', 'la paix', '2024-01-01', 0, 0, 0),
    ('ἡ εκκλησία', 'l''assemblée', '2024-01-01', 0, 0, 0),
    ('ἡ ἑσπερα', 'le soir', '2024-01-01', 0, 0, 0),
    ('ἑυρίσκω', 'je trouve', '2024-01-01', 0, 0, 0),
    ('ἡ ζωή', 'la vie, l''existence', '2024-01-01', 0, 0, 0),
    ('τό ζῷον', 'l''animal', '2024-01-01', 0, 0, 0),
    ('ὁ ἥλιος', 'le soleil', '2024-01-01', 0, 0, 0),
    ('ἡ ἡμέρα', 'le jour', '2024-01-01', 0, 0, 0),
    ('ὁ ἥπως', 'le héros', '2024-01-01', 0, 0, 0),
    ('ὁ θάνατος', 'la mort', '2024-01-01', 0, 0, 0),
    ('ἡ θεραπεία', 'le soin', '2024-01-01', 0, 0, 0),
    ('θερμός', 'chaud', '2024-01-01', 0, 0, 0),
    ('ἡ θυγάτηρ', 'la fille', '2024-01-01', 0, 0, 0),
    ('ὁ θύμος', 'le thym', '2024-01-01', 0, 0, 0),
    ('ὁ ἰατρός', 'le médecin', '2024-01-01', 0, 0, 0),
    ('ἱερός', 'sacré, saint', '2024-01-01', 0, 0, 0),
    ('ἰησῦς', 'Jésus', '2024-01-01', 0, 0, 0),
    ('ὁ ἵππος', 'le cheval', '2024-01-01', 0, 0, 0),
    ('ὁ ἰχτύς', 'le poisson', '2024-01-01', 0, 0, 0),
    ('κακός', 'mauvais', '2024-01-01', 0, 0, 0),
    ('τὸ κάρδαμον', 'le cresson', '2024-01-01', 0, 0, 0),
    ('ἡ κεφαλή', 'la tête', '2024-01-01', 0, 0, 0),
    ('κλέπτω', 'je vole, je dérobe', '2024-01-01', 0, 0, 0),
    ('ὁ κόσμος', 'le monde', '2024-01-01', 0, 0, 0),
    ('τό κράτος', 'le pouvoir, la force', '2024-01-01', 0, 0, 0),
    ('ὁ κύκλος', 'le cercle', '2024-01-01', 0, 0, 0),
    ('λευκός', 'blanc', '2024-01-01', 0, 0, 0),
    ('ὁ λίθος', 'la pierre', '2024-01-01', 0, 0, 0),
    ('λιπαρός', 'gras / opulent', '2024-01-01', 0, 0, 0),
    ('ἡ μάμμη', 'maman', '2024-01-01', 0, 0, 0),
    ('ὁ μάρτυρ', 'le témoin', '2024-01-01', 0, 0, 0),
    ('μέλας', 'noir', '2024-01-01', 0, 0, 0),
    ('τό μέλι', 'le miel', '2024-01-01', 0, 0, 0),
    ('τό μέσον', 'le milieu', '2024-01-01', 0, 0, 0),
    ('τό μέτρον', 'la mesure', '2024-01-01', 0, 0, 0),
    ('ἡ μήτηρ', 'la mère', '2024-01-01', 0, 0, 0),
    ('ἡ μηχανή', 'la machine, la ruse', '2024-01-01', 0, 0, 0),
    ('τό μίσος', 'la haine', '2024-01-01', 0, 0, 0),
    ('ὁ μῦθος', 'la légende, le récit', '2024-01-01', 0, 0, 0),
    ('μύριοι', 10000, '2024-01-01', 0, 0, 0),
    ('ὁ μῦς', 'le rat, la souris', '2024-01-01', 0, 0, 0),
    ('ὁ νόμος', 'la loi', '2024-01-01', 0, 0, 0),
    ('ἡ νύμφη', 'la jeune fille', '2024-01-01', 0, 0, 0),
    ('ὁ οἴκος', 'le clan, la maisonnée', '2024-01-01', 0, 0, 0),
    ('ὅλος', 'entier', '2024-01-01', 0, 0, 0),
    ('ὁμολογέω', 'je reconnais', '2024-01-01', 0, 0, 0),
    ('τό ὄναρ', 'le rêve', '2024-01-01', 0, 0, 0),
    ('τό ὄνομα', 'le nom', '2024-01-01', 0, 0, 0),
    ('τό ὅπλον', 'l''arme', '2024-01-01', 0, 0, 0),
    ('ἡ οργή', 'la colère', '2024-01-01', 0, 0, 0),
    ('ὁ ὄροφος', 'le toit', '2024-01-01', 0, 0, 0),
    ('ἡ ὄρχηστρις', 'la danceuse', '2024-01-01', 0, 0, 0),
    ('ὁ ὀφθαλμός', 'l''œil', '2024-01-01', 0, 0, 0),
    ('τό πάθος', 'l''émotion, la souffrance', '2024-01-01', 0, 0, 0),
    ('παράδοχος', 'bizarre, étrange', '2024-01-01', 0, 0, 0),
    ('τό πέλαγος', 'la haute mer', '2024-01-01', 0, 0, 0),
    ('ἡ μέτρα', 'le rocher', '2024-01-01', 0, 0, 0),
    ('ἡ πληγή', 'le coup', '2024-01-01', 0, 0, 0),
    ('τό πνεῦμα', 'le souffle, l''esprit', '2024-01-01', 0, 0, 0),
    ('ὁ πόλεμος', 'la guerre', '2024-01-01', 0, 0, 0),
    ('ὁ ποταμός', 'le fleuve', '2024-01-01', 0, 0, 0),
    ('τό ποτόν', 'la boisson', '2024-01-01', 0, 0, 0),
    ('ὁ πρέσβυς', 'la personne âgée / l''ambassadeur', '2024-01-01', 0, 0, 0),
    ('τό προθυρον', 'le vestibule', '2024-01-01', 0, 0, 0),
    ('τό πτερόν', 'la plume, l''aile', '2024-01-01', 0, 0, 0),
    ('ὁ ῥήτωπ', 'l''orateur', '2024-01-01', 0, 0, 0),
    ('τό ῥόδον', 'la rose', '2024-01-01', 0, 0, 0),
    ('ὁ ῥυθμός', 'le rythme, la mesure', '2024-01-01', 0, 0, 0),
    ('σαφής', 'clair, manifeste', '2024-01-01', 0, 0, 0),
    ('ἡ σελήνη', 'la lune', '2024-01-01', 0, 0, 0),
    ('σκληρός', 'rude, dur', '2024-01-01', 0, 0, 0),
    ('σπειρω', 'je sème', '2024-01-01', 0, 0, 0),
    ('ὁ στέφανος', 'la couronne', '2024-01-01', 0, 0, 0),
    ('τό στόμα', 'la bouche', '2024-01-01', 0, 0, 0),
    ('ὁ στρατηγός', 'le général', '2024-01-01', 0, 0, 0),
    ('τό σχημα', 'la figure, le registre', '2024-01-01', 0, 0, 0),
    ('ἡ σκολή', 'le loisir, le temps libre', '2024-01-01', 0, 0, 0),
    ('τό τέρας', 'le monstre', '2024-01-01', 0, 0, 0),
    ('ἡ τέχνη', 'l''art', '2024-01-01', 0, 0, 0),
    ('ἡ τράπηζα', 'la table', '2024-01-01', 0, 0, 0),
    ('ὑγιενός', 'sain, salutaire', '2024-01-01', 0, 0, 0),
    ('ὁ ὕπνος', 'le sommeil', '2024-01-01', 0, 0, 0),
    ('ὑπό', 'sous', '2024-01-01', 0, 0, 0),
    ('τό φάρμακον', 'le remède / le poison', '2024-01-01', 0, 0, 0),
    ('φιλέω', 'j''aime', '2024-01-01', 0, 0, 0),
    ('ὁ φόβος', 'la peur', '2024-01-01', 0, 0, 0),
    ('τό φύλλον', 'la feuille', '2024-01-01', 0, 0, 0),
    ('ἡ φύσις', 'la nature / l''origine', '2024-01-01', 0, 0, 0),
    ('τό φυτόν', 'la plante', '2024-01-01', 0, 0, 0),
    ('ἡ φωνή', 'la voix', '2024-01-01', 0, 0, 0),
    ('τό φῶς', 'la lumière', '2024-01-01', 0, 0, 0),
    ('χίλιοι', 1000, '2024-01-01', 0, 0, 0),
    ('ἡ χορδή', 'l''intestin / la corde', '2024-01-01', 0, 0, 0),
    ('ὁ χορός', 'la danse / le chœur', '2024-01-01', 0, 0, 0),
    ('ὁ χρόσος', 'le temps', '2024-01-01', 0, 0, 0),
    ('ὁ χρύσος', 'l''or', '2024-01-01', 0, 0, 0),
    ('ψάλλω', 'je joue', '2024-01-01', 0, 0, 0),
    ('ψιλός', 'simple', '2024-01-01', 0, 0, 0),
    ('ἡ ψυχή', 'l''âme', '2024-01-01', 0, 0, 0),
    ('ἡ ᾠδή', 'le chant', '2024-01-01', 0, 0, 0),
    ('ἡ ὥπα', 'l''heure', '2024-01-01', 0, 0, 0),
    ('ωχπός', 'jaune pâle', '2024-01-01', 0, 0, 0),
    ('φαινομαι', 'j''apparais (comme)', '2024-01-01', 0, 0, 0),
    ('σκοπῶ', 'j''observe', '2024-01-01', 0, 0, 0),
    ('σκππκός', 'qui observe', '2024-01-01', 0, 0, 0),
    ('πρό', 'avant / devant', '2024-01-01', 0, 0, 0),
    ('ὕστεπος', 'après / plus tard', '2024-01-01', 0, 0, 0),
    ('ἱστορίαι', 'l''enquête, les recherches', '2024-01-01', 0, 0, 0),
    ('ὁ πούς', 'le pied', '2024-01-01', 0, 0, 0),
    ('κινῶ', 'je mets en mouvement', '2024-01-01', 0, 0, 0),
    ('μετέχω', 'je participe', '2024-01-01', 0, 0, 0),
    ('τὸ στάδιον', 'la mesure', '2024-01-01', 0, 0, 0),
    ('ὁπμάομαι', 'je m''élance', '2024-01-01', 0, 0, 0),
    ('σημαίνω', 'faire signe / signifier', '2024-01-01', 0, 0, 0),
    ('ὁ πολύπους', 'le poulpe', '2024-01-01', 0, 0, 0);



/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
