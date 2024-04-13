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
CREATE DATABASE wh0_Are_y0u_arabic;
USE wh0_Are_y0u_arabic;



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
    arabic CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    français CHAR(255),
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
    arabic CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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

CREATE TABLE IF NOT EXISTS archive (
	id_word SMALLINT AUTO_INCREMENT PRIMARY KEY,
    arabic CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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
INSERT INTO `version_voc` (`arabic`, `français`, `creation_date`, `nb`, `score`, `taux`) VALUES
	('إلتقى', 'Se retrouver', 0, 0, 0, 0),
	('النّاسِ', 'les gens', 0, 0, 0, 0),
	('المُوَظَّف', 'employé', 0, 0, 0, 0),
	('عدد كبير من', 'un grand nombre de', 0, 0, 0, 0),
	('على الأقدام', '(marche) à pied', 0, 0, 0, 0),
	('اليوم التالي', 'le jour suivant', 0, 0, 0, 0),
	('حاليّاً', 'actuellement', 0, 0, 0, 0),
	('المفتاح', 'clé', 0, 0, 0, 0),
	('رُبَّـمَا', 'peut-être', 0, 0, 0, 0),
	('كفى', 'suffire', 0, 0, 0, 0),
	('شغل', 'travailler comme', 0, 0, 0, 0),
	('الجِهَاز', 'appareil, poste, instrument', 0, 0, 0, 0),
	('بالضبط', 'exactement', 0, 0, 0, 0),
	('مَرّةً أُخْرى', 'encore une fois', 0, 0, 0, 0),
	('دَوْر', 'tour, rôle', 0, 0, 0, 0),
	('مُتَرَدِّدٌ', 'hésitant', 0, 0, 0, 0),
	('الإِنْتَرْنِت', 'internet', 0, 0, 0, 0),
	('الوقُوف', 'arrêt, stationnement', 0, 0, 0, 0),
	('زِيّت', 'huile', 0, 0, 0, 0),
	('يَحَتاجُ إِلَى', 'avoir besoin de', 0, 0, 0, 0),
	('يَقْبَلُ', 'accepter', 0, 0, 0, 0),
	('نِسْبِيّاً', 'relativement', 0, 0, 0, 0),
	('مَضْبُوط', 'exact', 0, 0, 0, 0),
	('وَطَنِي', 'national', 0, 0, 0, 0),
	('الـخَرِيف', 'l''automne', 0, 0, 0, 0),
	('المَعِدَة', 'estomac', 0, 0, 0, 0),
	('يُقَيِّمُ', 'estimer', 0, 0, 0, 0),
	('المُواصِلة', 'poursuite', 0, 0, 0, 0),
	('آلة تَصوِير', 'appareil photo', 0, 0, 0, 0),
	('نَتيجَة', 'résultat', 0, 0, 0, 0),
	('مُخَصّص ل', 'réservé à, consacré à', 0, 0, 0, 0),
	('الخَطِيب', 'fiancé', 0, 0, 0, 0),
	('المِلْح', 'sel', 0, 0, 0, 0),
	('سُكَّر', 'sucre', 0, 0, 0, 0),
	('دَعْوَة', 'invitation', 0, 0, 0, 0),
	('المَعْرِفَة', 'des connaissances (personnes)', 0, 0, 0, 0),
	('للأسفِ', 'malheureusement', 0, 0, 0, 0),
	('البَساطة', 'simplicité', 0, 0, 0, 0),
	('العَرْض', 'offre, proposition', 0, 0, 0, 0),
	('الاِحْتِرام', 'respect', 0, 0, 0, 0),
	('صِحَّة', 'santé', 0, 0, 0, 0),
	('بلَّغ', 'transmettre', 0, 0, 0, 0),
	('خلَّد', 'honorer', 0, 0, 0, 0),
	('الأُخُوَّة', 'fraternité', 0, 0, 0, 0),
	('صَحَافَة', 'presse', 0, 0, 0, 0),
	('آسِف', 'désolé', 0, 0, 0, 0),
	('أَسْوَد', 'noir', 0, 0, 0, 0),
	('متسخ', 'sale', 0, 0, 0, 0),
	('أضاف', 'ajouter', 0, 0, 0, 0),
	('كَرَم', 'générosité', 0, 0, 0, 0),
	('رِيَاضِيّ', 'sportif', 0, 0, 0, 0),
	('المُدِير', 'directeur', 0, 0, 0, 0),
	('دَفْتَرُ', 'carnet, cahier', 0, 0, 0, 0),
	('نَصِيحَة', 'conseil', 0, 0, 0, 0),
	('الحَبَّة', 'grain, pilule, céréale', 0, 0, 0, 0),
	('مُصَادَقَة', 'par hasard', 0, 0, 0, 0),
	('الجائِزَة', 'prix, récompense', 0, 0, 0, 0),
	('اِسْتِثْنَائِيّ', 'exceptionnel', 0, 0, 0, 0),
	('حركة المرور', 'circulation', 0, 0, 0, 0),
	('رُبْع ساعة', 'quart d''heure', 0, 0, 0, 0),
	('المُسْتَوَى', 'niveau', 0, 0, 0, 0),
	('الاِنْفِعال', 'humeur, émotion', 0, 0, 0, 0),
	('مـَمْنُوع', 'interdit', 0, 0, 0, 0),
	('المَصارِف', 'banque', 0, 0, 0, 0),
	('سَائِح', 'touriste', 0, 0, 0, 0),
	('العُمْلَة', 'monnaie, devise', 0, 0, 0, 0),
	('راعٍ', 'berger', 0, 0, 0, 0),
	('الرَّبِيع', 'le printemps', 0, 0, 0, 0),
	('عثر على', 'tomber sur, trouver par hasard', 0, 0, 0, 0),
	('سَطْح', 'terrasse, espace', 0, 0, 0, 0),
	('طَبِيعَةٌ', 'la nature', 0, 0, 0, 0),
	('وَراءَ', 'derrière', 0, 0, 0, 0),
	('خَلَع', 'enlever, ôter, enlever', 0, 0, 0, 0),
	('يَقِفُ', 'être debout, s''arrêter', 0, 0, 0, 0),
	('عَلَى وَشْكِ', 'sur le point de', 0, 0, 0, 0),
	('الغَابَة', 'forêt', 0, 0, 0, 0),
	('شَكْل', 'forme, motif, dessin', 0, 0, 0, 0),
	('لِصّ', 'brigand, voleur, bandit', 0, 0, 0, 0),
	('الإجراء', 'mesure politique', 0, 0, 0, 0),
	('هاجم', 'attaquer', 0, 0, 0, 0),
	('كَامِل', 'entier', 0, 0, 0, 0),
	('واخِز', 'intense', 0, 0, 0, 0),
	('المَقْطوع', 'extrait', 0, 0, 0, 0),
	('الغِيَاب', 'absence de, manque', 0, 0, 0, 0),
	('الكَشْف', 'révélation', 0, 0, 0, 0),
	('بالمُقابِل', 'en contrepartie de', 0, 0, 0, 0),
	('الوَجَع', 'douleur', 0, 0, 0, 0),
	('فَائِق', 'supérieur', 0, 0, 0, 0),
	('ظَهِر', 'apparaître', 0, 0, 0, 0),
	('الإِعْلان', 'annonce', 0, 0, 0, 0),
	('الهَوِيَّة', 'identité', 0, 0, 0, 0),
	('مَلأ', 'remplir', 0, 0, 0, 0),
	('مُنْسَجِم', 'harmonieux', 0, 0, 0, 0),
	('نام', 'dormir', 0, 0, 0, 0),
	('الفَوْضَى', 'anarchie, désordre', 0, 0, 0, 0),
	('سنة الجديدة', 'la nouvelle année', 0, 0, 0, 0),
	('على أي حال', 0, 0, 0, 0, 0),
	('مُرْسَلَ إلَيْهِ', 'destinataire', 0, 0, 0, 0),
	('البَدَايَة', 'début', 0, 0, 0, 0),
	('صُنْدُوق بريدي', 'boîte postale', 0, 0, 0, 0),
	('بَرِيدٌ صَوْتِيّ', 'boîte vocale', 0, 0, 0, 0),
	('مُنْتَشِر', 'répandu', 0, 0, 0, 0),
	('خُفْيَةً', 'en cachette', 0, 0, 0, 0),
	('المَساء', 'soir', 0, 0, 0, 0),
	('بَعْض', 'quelque', 0, 0, 0, 0),
	('جاء', 'venir', 0, 0, 0, 0),
	('يُنْفِقُ', 'dépenser', 0, 0, 0, 0),
	('التي', 'laquelle', 0, 0, 0, 0),
	('لا شكر على واجب ', 'de rien', 0, 0, 0, 0),
	('بدا', 'il semble que', 0, 0, 0, 0),
	('مَعًا', 'ensemble', 0, 0, 0, 0),
	('الأَمام', 'devant', 0, 0, 0, 0),
	('غَداً', 'demain', 0, 0, 0, 0),
	('نَشَاط', 'activité', 0, 0, 0, 0),
	('إِنْسَانٌ', 'être humain', 0, 0, 0, 0),
	('بَضَائِع', 'biens', 0, 0, 0, 0),
	('حاسوب', 'ordinateur', 0, 0, 0, 0),
	('ذهابا وإيابا', 'aller retour', 0, 0, 0, 0),
	('سِعْر', 'prix', 0, 0, 0, 0),
	('يَبْحَثُ عَنْ', 'chercher', 0, 0, 0, 0),
	('أود أن', 'je voudrais', 0, 0, 0, 0),
	('قفطان', 'caftan (pour les femmes au Maroc)', 0, 0, 0, 0),
	('مُجَامِل', 'gratuit', 0, 0, 0, 0),
	('أبدا', 'pas du tout', 0, 0, 0, 0),
	('أرجوك', 'je te prie', 0, 0, 0, 0),
	('لا شكّ أنّ', '"Pas de doute que …"', 0, 0, 0, 0),
	('بلا', 'sans', 0, 0, 0, 0),
	('باِلإضَافَة إِلى', 'en outre', 0, 0, 0, 0),
	('الـمُحِيط الأَطْلَسِي', 'océan Atlantique', 0, 0, 0, 0),
	('حَفْلَةٌ', 'fête, cérémonie', 0, 0, 0, 0),
	('أسرع', 'dépêche-toi !', 0, 0, 0, 0),
	('لا يهم', 'ce n''est pas important', 0, 0, 0, 0),
	('فُسْتَان', 'robe', 0, 0, 0, 0),
	('إذا ', 'si', 0, 0, 0, 0),
	('مُسْتَمِرّ', 'constant, continu', 0, 0, 0, 0),
	('تَارِيخ', 'histoire', 0, 0, 0, 0),
	('نوع', 'catégorie, genre', 0, 0, 0, 0),
	('نَفْس', 'âme, être, individu', 0, 0, 0, 0),
	('إِلى آخِرِه', 'et caetera', 0, 0, 0, 0),
	('كَلِمَة', 'mot', 0, 0, 0, 0),
	('صَعْب', 'difficile', 0, 0, 0, 0),
	('صَحِيح', 'vrai, sain', 0, 0, 0, 0),
	('مِكنَسَة', 'balai', 0, 0, 0, 0),
	('بعيد عن', 'près de', 0, 0, 0, 0),
	('شُرْفَة', 'balcon', 0, 0, 0, 0),
	('جَوْهَرَة', 'bijou', 0, 0, 0, 0),
	('مَطْبَخ', 'cuisine', 0, 0, 0, 0),
	('عالٍ', 'haut, élevé', 0, 0, 0, 0),
	('خبر', 'nouvelle', 0, 0, 0, 0),
	('يُسَجِّلُ', 'enregistrer', 0, 0, 0, 0),
	('عَاجِل', 'urgent', 0, 0, 0, 0),
	('تخفيض', 'réduction', 0, 0, 0, 0),
	('طَائِرَة', 'avion', 0, 0, 0, 0),
	('واسِع', 'vaste', 0, 0, 0, 0),
	('تَذْكِرَة', 'billet', 0, 0, 0, 0),
	('حَقِيبَةُ سَفَر', 'valise (de voyage)', 0, 0, 0, 0),
	('آخر', 'autre', 0, 0, 0, 0),
	('نِسْبة', 'taux', 0, 0, 0, 0),
	('أمّ', 'mère', 0, 0, 0, 0),
	('الباص', 'autobus', 0, 0, 0, 0),
	('فلاح', 'paysan', 0, 0, 0, 0),
	('مُفَضَّل', 'préféré', 0, 0, 0, 0),
	('طويِل', 'long', 0, 0, 0, 0),
	('صغير', 'petit', 0, 0, 0, 0),
	('ركب', 'monter dans un véhicule', 0, 0, 0, 0),
	('إنتظار', 'attente', 0, 0, 0, 0),
	('يُقَابِلُ', 'rencontrer', 0, 0, 0, 0),
	('مَحْظُوظ', 'chanceux', 0, 0, 0, 0),
	('اليمين', 'la droite', 0, 0, 0, 0),
	('عَصِيرُ بُرْتُقَالٍ', 'jus d''orange', 0, 0, 0, 0),
	('غُرُوبُ الشَّمْس', 'coucher de soleil', 0, 0, 0, 0),
	('مَنارَة', 'minaret', 0, 0, 0, 0),
	('معجز', 'miraculeux', 0, 0, 0, 0),
	('شايٌ مَع نَعْناعٍ', 'thé à la menthe', 0, 0, 0, 0),
	('الفَجْر', 'aube', 0, 0, 0, 0),
	('بَقِيَ', 'rester', 0, 0, 0, 0),
	('رفع', 'soulever', 0, 0, 0, 0),
	('فَوْق', 'en haut, au-dessus', 0, 0, 0, 0),
	('نَصّ', 'texte', 0, 0, 0, 0),
	('عَالَم', 'monde', 0, 0, 0, 0),
	('حَجَر', 'pierre', 0, 0, 0, 0),
	('تعال', 'Viens !', 0, 0, 0, 0),
	('مَقْعَد', 'siège', 0, 0, 0, 0),
	('يَتَمَنَّى', 'souhaiter', 0, 0, 0, 0),
	('طرد', 'paquet', 0, 0, 0, 0),
	('بَلَد', 'pays', 0, 0, 0, 0),
	('مُخْتَلِف', 'différent', 0, 0, 0, 0),
	('هكذا', 'ainsi', 0, 0, 0, 0),
	('خاصّ', 'particulier', 0, 0, 0, 0),
	('هرب', 's''enfuir', 0, 0, 0, 0),
	('غَضْبَان', 'fâché', 0, 0, 0, 0),
	('ضَوئيّ', 'lumineux', 0, 0, 0, 0),
	('دفع', 'payer', 0, 0, 0, 0),
	('بالقُرْب', 'à proximité', 0, 0, 0, 0),
	('وَزير', 'ministre', 0, 0, 0, 0),
	('فَم', 'bouche', 0, 0, 0, 0),
	('أَنْف', 'nez', 0, 0, 0, 0),
	('وَحْد', 'seul', 0, 0, 0, 0),
	('نور', 'lumière', 0, 0, 0, 0),
	('طَعام', 'nourriture', 0, 0, 0, 0),
	('ملابس', 'vêtements', 0, 0, 0, 0),
	('زَبون', 'client', 0, 0, 0, 0),
	('متعَب', 'fatigué', 0, 0, 0, 0),
	('حسْناً', 'bien !', 0, 0, 0, 0),
	('فقط', 'seulement', 0, 0, 0, 0),
	('غالٍ', 'cher (coûteux)', 0, 0, 0, 0),
	('يَوْمُ الـخَمِيس', 'jeudi', 0, 0, 0, 0),
	('يَوْمُ الثُّلَاثَاء', 'mardi', 0, 0, 0, 0),
	('يوم الـجُمْعَة', 'vendredi', 0, 0, 0, 0),
	('يوم الاثنين', 'lundi', 0, 0, 0, 0),
	('المسجد', 'mosquée', 0, 0, 0, 0),
	('اليومَ', 'aujourd''hui', 0, 0, 0, 0),
	('وسط, مركز', 'centre', 0, 0, 0, 0),
	('فرِح', 'se réjouir', 0, 0, 0, 0),
	('عامّ', 'public, général', 0, 0, 0, 0),
	('سَبَب', 'cause', 0, 0, 0, 0),
	('بسبب', 'à cause de', 0, 0, 0, 0),
	('غسل', 'laver', 0, 0, 0, 0),
	('منطقة', 'région', 0, 0, 0, 0),
	('حيّ', 'quartier', 0, 0, 0, 0),
	('أسبوع', 'semaine', 0, 0, 0, 0),
	('ابدا', 'pas du tout, jamais', 0, 0, 0, 0),
	('قادم', 've0t', 0, 0, 0, 0),
	(' قديم', 'vieux', 0, 0, 0, 0),
	('مَسْرور', 'joyeux, content', 0, 0, 0, 0),
	('شخص', 'personne', 0, 0, 0, 0),
	('شرب', 'boire', 0, 0, 0, 0),
	('عرف', 'connaître, savoir', 0, 0, 0, 0),
	('شارع', 'rue', 0, 0, 0, 0),
	('فهِم', 'comprendre', 0, 0, 0, 0),
	('صوت', 'voix, bruit, son', 0, 0, 0, 0),
	('دواء', 'médicament, remède', 0, 0, 0, 0),
	('هجرة', 'émigration, l''Hégire (622)', 0, 0, 0, 0),
	('حاجة', 'besoin', 0, 0, 0, 0),
	('يوم الاحد', 'dimanche', 0, 0, 0, 0),
	('غُبَار', 'poussière', 0, 0, 0, 0),
	('جيّد', 'bon', 0, 0, 0, 0),
	('متى ؟', 'quand … ?', 0, 0, 0, 0),
	('هنا', 'ici', 0, 0, 0, 0),
	('هناك', 'là', 0, 0, 0, 0),
	('فَوْراً', 'immédiatement', 0, 0, 0, 0),
	('مريض', 'malade', 0, 0, 0, 0),
	('خير', 'bien', 0, 0, 0, 0),
	('ساعة', 'montre, heure', 0, 0, 0, 0),
	('إجتماع', 'réunion', 0, 0, 0, 0),
	('لحم', 'viande', 0, 0, 0, 0),
	('سمك', 'poisson (collectif)', 0, 0, 0, 0),
	('نقود', 'argent (liquide)', 0, 0, 0, 0),
	('ماء', 'eau', 0, 0, 0, 0),
	('مُتْعِب', 'fatigant', 0, 0, 0, 0),
	('نَفِيس', 'précieux', 0, 0, 0, 0),
	('خبز', 'pain', 0, 0, 0, 0),
	('فُنْدُق', 'hôtel', 0, 0, 0, 0),
	('نزل', 'descendre', 0, 0, 0, 0),
	('مطعم', 'restaurant', 0, 0, 0, 0),
	(' اليوم الغدا', 'le lendemain', 0, 0, 0, 0),
	('تاجِر', 'commerçant', 0, 0, 0, 0),
	('رخيص', 'bon marché', 0, 0, 0, 0),
	('بين', 'entre', 0, 0, 0, 0),
	('ماضٍ', 'passé', 0, 0, 0, 0),
	('يوم الأربعاء', 'mercredi', 0, 0, 0, 0),
	('يوم السبت', 'samedi', 0, 0, 0, 0),
	('شاطِئ', 'plage', 0, 0, 0, 0),
	('حُضُور', 'présence, assistance à', 0, 0, 0, 0),
	('رجا', 'prier (qn), demander', 0, 0, 0, 0),
	(' المَدْعُوّ', 'invité', 0, 0, 0, 0),
	('أَمْتِعَة', 'bagages', 0, 0, 0, 0),
	('أقلع', 'décoller (IV)', 0, 0, 0, 0),
	('يُناسِبُ', 'convenir, correspondre à', 0, 0, 0, 0),
	('إضافةً على ذلك ', 'en plus de cela', 0, 0, 0, 0),
	('يُوَفِّرُ', 'économiser', 0, 0, 0, 0),
	('فُرَاقٌ', 'séparation', 0, 0, 0, 0),
	('مُغادَرَة', 'départ', 0, 0, 0, 0),
	('قُبْلَة', 'un baiser', 0, 0, 0, 0),
	('بواسِطة', 'au moyen de', 0, 0, 0, 0),
	('يحكي', 'raconter', 0, 0, 0, 0),
	('حساب', 'addition, compte', 0, 0, 0, 0),
	('شركة', 'entreprise', 0, 0, 0, 0),
	('عادَة', 'd''habitude', 0, 0, 0, 0),
	('مثل', 'comme', 0, 0, 0, 0),
	(' ماذا ؟', 'quoi ?', 0, 0, 0, 0),
	('شَابّ', 'jeune homme', 0, 0, 0, 0),
	('قطار', 'train', 0, 0, 0, 0),
	('شَهْر', 'mois', 0, 0, 0, 0),
	('قائمة', 'liste', 0, 0, 0, 0),
	('حافظة نقود', 'portefeuille', 0, 0, 0, 0),
	('قَبْلَ', 'avant', 0, 0, 0, 0),
	('نظِر إلى', 'regarder (vers)', 0, 0, 0, 0),
	('تسجيل', 'inscription (enregistrement)', 0, 0, 0, 0),
	('شتاء', 'hiver', 0, 0, 0, 0),
	('أَمْر', 'ordre', 0, 0, 0, 0),
	('غرفة استقبال', 'salon de réception', 0, 0, 0, 0),
	('مغرٍ', 'intéressant, avantageux', 0, 0, 0, 0),
	('مُتَجَمِّد', 'gelé', 0, 0, 0, 0),
	('ثوب', 'vêtement, habit, manteau', 0, 0, 0, 0),
	('سمع', 'écouter', 0, 0, 0, 0),
	('ضرب', 'frapper', 0, 0, 0, 0),
	('ضحك', 'rire', 0, 0, 0, 0),
	('رِحْلَة', 'vol, périple', 0, 0, 0, 0),
	('فتح', 'ouvrir', 0, 0, 0, 0),
	(' لحظة', 'un instant', 0, 0, 0, 0),
	('مطار', 'aéroport', 0, 0, 0, 0),
	('مبلغ', 'somme, montant', 0, 0, 0, 0),
	('نصف', 'moitié', 0, 0, 0, 0),
	('مستعجل', 'pressé', 0, 0, 0, 0),
	('شباك', 'guichet', 0, 0, 0, 0),
	('حجز', 'réserver', 0, 0, 0, 0),
	('إستئجار', 'louer (un appartement)', 0, 0, 0, 0),
	('إستعار', 'emprunter', 0, 0, 0, 0),
	('تَقْليد', 'coutume', 0, 0, 0, 0),
	('تطور', 'se développer', 0, 0, 0, 0),
	('صَحِيفَة', 'journal', 0, 0, 0, 0),
	('نقل', 'transporter', 0, 0, 0, 0),
	('إخلاء', 'évacuation (fait d''évacuer)', 0, 0, 0, 0),
	('اتّصل', 'prendre contact', 0, 0, 0, 0),
	('شبه', 'ressembler (intransitif)', 0, 0, 0, 0),
	('النَّجْدَة', 'A l''aide !', 0, 0, 0, 0),
	('غَرامة', 'amende, pénalité', 0, 0, 0, 0),
	('عُبُور', 'traversée', 0, 0, 0, 0),
	('ضِيافة', 'hospitalité', 0, 0, 0, 0),
	('نجاح', 'succès, réussite', 0, 0, 0, 0),
	('يَبْدَأُ', 'commencer', 0, 0, 0, 0),
	('صباح', 'matin', 0, 0, 0, 0),
	('أصبح', 'devenir', 0, 0, 0, 0),
	('عنوان', 'adresse (domicile) / titre d''un livre', 0, 0, 0, 0),
	(' بِطاقة', 'carte (bancaire, de visite, d''étudiant, …)', 0, 0, 0, 0),
	('كُلّ', 'chaque (masc.)', 0, 0, 0, 0),
	('ضَيِّق', 'étroit', 0, 0, 0, 0),
	('قال', 'dire', 0, 0, 0, 0),
	('الذّين', 'lesquels', 0, 0, 0, 0),
	('شرطة', 'police', 0, 0, 0, 0),
	('إنطلق', 'démarrer, partir', 0, 0, 0, 0),
	('طلق', 'lâcher, libérer', 0, 0, 0, 0),
	('أَوَّلاً', 'premièrement', 0, 0, 0, 0),
	('مَلْعَب', 'stade (sportif)', 0, 0, 0, 0),
	('إِنْتَظِر !', 'attends !', 0, 0, 0, 0),
	('أزرق', 'bleu', 0, 0, 0, 0),
	('أَصْفَر', 'jaune', 0, 0, 0, 0),
	('أَخْضَر', 'vert', 0, 0, 0, 0),
	('أَحْمَر', 'rouge', 0, 0, 0, 0),
	('أَبْيَض', 'blanc', 0, 0, 0, 0),
	('سِعْر / ثَمَن', 'prix, coût', 0, 0, 0, 0),
	('صَرّاف', 'bureau de change', 0, 0, 0, 0),
	('بطاقة الائتمان', 'carte de crédit', 0, 0, 0, 0),
	(' أي', 'c''est-à-dire', 0, 0, 0, 0),
	('يورو ', 'euro', 0, 0, 0, 0),
	('نقدا', 'en argent liquide', 0, 0, 0, 0),
	('كافية', 'suffisant', 0, 0, 0, 0),
	('يَعَاوَن', 'collaborer, s''entraider', 0, 0, 0, 0),
	('مَحَلِيّ', 'local (adjectif)', 0, 0, 0, 0),
	('سماء', 'ciel', 0, 0, 0, 0),
	('الغَنَم', 'le mouton', 0, 0, 0, 0),
	('ثلج', 'neige', 0, 0, 0, 0),
	('سلّم', 'remettre à, confier', 0, 0, 0, 0),
	('بالتأكيد !', 'pour sûr !', 0, 0, 0, 0),
	('تبِع', 'suivre', 0, 0, 0, 0),
	('طابور', 'queue, colonne, file', 0, 0, 0, 0),
	('نِهاية الُأسْبوع', 'weekend', 0, 0, 0, 0),
	('رائع', 'extraordinaire', 0, 0, 0, 0),
	('هَدِيَّة', 'cadeau', 0, 0, 0, 0),
	('مستحيل', 'impossible', 0, 0, 0, 0),
	('عِنْدَما', 'quand, lorsque', 0, 0, 0, 0),
	('رقص', 'danser', 0, 0, 0, 0),
	('جَبَل', 'montagne', 0, 0, 0, 0),
	('شهَد', 'voir, être témoin de, assister à', 0, 0, 0, 0),
	('كلام', 'langage', 0, 0, 0, 0),
	('جمع', 'rassembler', 0, 0, 0, 0),
	('جمّع', 'assembler', 0, 0, 0, 0),
	('يَجْمَعُ', 'se rassembler', 0, 0, 0, 0),
	('شباب', 'jeunesse', 0, 0, 0, 0),
	('مُحَام', 'avocat', 0, 0, 0, 0),
	('منذ', 'depuis', 0, 0, 0, 0),
	('نسي', 'oublier', 0, 0, 0, 0),
	('أَجْنَبيّ', 'étranger', 0, 0, 0, 0),
	('الـخَارِج', 'l''étranger', 0, 0, 0, 0),
	('مَمنُن', 'reconnaissant', 0, 0, 0, 0),
	('إلى اللقاء', 'au revoir', 0, 0, 0, 0),
	('سنة', 'année', 0, 0, 0, 0),
	('حَيْثُ', 'où …', 0, 0, 0, 0),
	('أعطى', 'donner, offrir', 0, 0, 0, 0),
	('قصر', 'palais, place-forte', 0, 0, 0, 0),
	('لا تحصى', 'innombrable', 0, 0, 0, 0),
	('يسار', 'gauche', 0, 0, 0, 0),
	('مَحَطَة', 'station', 0, 0, 0, 0),
	('رغِبَ', 'déisirer', 0, 0, 0, 0),
	('قيمة', 'valeur', 0, 0, 0, 0),
	('اخيرا', 'enfin', 0, 0, 0, 0),
	('واجهة', 'vitrine', 0, 0, 0, 0),
	(' زار', 'rendre visite', 0, 0, 0, 0),
	('خَال', 'oncle (côté maternel)', 0, 0, 0, 0),
	('عَمّ', 'oncle (côté paternel)', 0, 0, 0, 0),
	('طلب', 'demander', 0, 0, 0, 0),
	('ضَخْم', 'énorme', 0, 0, 0, 0),
	('طالب', 'étudiant', 0, 0, 0, 0),
	('أب', 'père', 0, 0, 0, 0),
	('مبنى ', 'immeuble', 0, 0, 0, 0),
	('رأس', 'tête', 0, 0, 0, 0),
	('سعيد', 'heureux', 0, 0, 0, 0),
	('نظف', 'nettoyer', 0, 0, 0, 0),
	('سَرير', 'lit', 0, 0, 0, 0),
	('بِساط', 'tapis', 0, 0, 0, 0),
	('شاعر', 'poète', 0, 0, 0, 0),
	('باب', 'porte', 0, 0, 0, 0),
	('جَرِّب', 'essayer', 0, 0, 0, 0),
	('مَوْسِم', 'saison', 0, 0, 0, 0),
	('مُسْتَوْصَف', 'dispensaire', 0, 0, 0, 0),
	('اِخْتِلَاف', 'différence', 0, 0, 0, 0),
	('إستفاد', 'bénéficier', 0, 0, 0, 0),
	('بِمُعْظَمِهِ', 'pour sa plus grande part', 0, 0, 0, 0),
	('رغما عن', 'malgré', 0, 0, 0, 0),
	('آسِيَا', 'Asie', 0, 0, 0, 0),
	('عيادة', 'clinique', 0, 0, 0, 0),
	('رَفيع', 'éminent, raffiné, élevé', 0, 0, 0, 0),
	('تأشيرة', 'visa', 0, 0, 0, 0),
	('ترك', 'laisser, abandonner', 0, 0, 0, 0),
	(0, 'écoeurement, nausée', 0, 0, 0, 0),
	(0, 'constater, observer, remarquer', 0, 0, 0, 0),
	('الْعُصُورُ الْوُسْطَى', 'le Moyen-Âge', 0, 0, 0, 0),
	('نافِذة ', 'fenêtre', 0, 0, 0, 0),
	('ربح', 'bénéfice', 0, 0, 0, 0),
	('تضحية', 'sacrifice', 0, 0, 0, 0),
	('إزدحام', 'embouteillage', 0, 0, 0, 0),
	('مَسافَة', 'distance', 0, 0, 0, 0),
	('إخطار', 'avertissement', 0, 0, 0, 0),
	('إتجاه', 'direction', 0, 0, 0, 0),
	('ختاماً', 'pour finir', 0, 0, 0, 0),
	('إذا', 'si, au cas où', 0, 0, 0, 0),
	('خارِج ', 'dehors, à l''extérieur', 0, 0, 0, 0),
	('حديد', 'fer', 0, 0, 0, 0),
	('المساومة', 'marchandage, tractation', 0, 0, 0, 0),
	('إستقبال', 'réception, accueil', 0, 0, 0, 0),
	('لون', 'couleur', 0, 0, 0, 0),
	('حاول', 'essayer', 0, 0, 0, 0),
	('تحضير', 'préparation', 0, 0, 0, 0),
	('رَقَم', 'numéro', 0, 0, 0, 0),
	('إعلام عن', 'déclaration (de vol, de perte)', 0, 0, 0, 0),
	('كيس', 'sac', 0, 0, 0, 0),
	('شيك', 'chèque', 0, 0, 0, 0),
	('على الرّأس العين', 'bien volontiers !', 0, 0, 0, 0),
	('بِداية', 'début', 0, 0, 0, 0),
	('إستراح', 'se reposer', 0, 0, 0, 0),
	('نصب', 'planter (une tente)', 0, 0, 0, 0),
	('خيمة', 'tente', 0, 0, 0, 0),
	('نار', 'feu', 0, 0, 0, 0),
	('خطب', 'prêcher / demander en mariage', 0, 0, 0, 0),
	('مستشفى', 'hôpital', 0, 0, 0, 0),
	('وقت', 'temps, moment', 0, 0, 0, 0),
	('تسوق', 'shopping', 0, 0, 0, 0),
	('أزهر', 'resplendissant', 0, 0, 0, 0),
	('شراء', 'achat', 0, 0, 0, 0),
	(' يوما ما', 'un certain jour', 0, 0, 0, 0),
	('هاتف', 'téléphone', 0, 0, 0, 0),
	('إمتلك', 'posséder', 0, 0, 0, 0),
	('ملك', 'roi', 0, 0, 0, 0),
	('هندسة', 'ingénieurie', 0, 0, 0, 0),
	('فارِغ', 'vide', 0, 0, 0, 0),
	('تحت', 'sous', 0, 0, 0, 0),
	('طبعا', 'naturellement', 0, 0, 0, 0),
	('هَمّ', 'souci, préoccupation', 0, 0, 0, 0),
	('بل', 'bien plus, et même', 0, 0, 0, 0),
	('إِنْفَاق', 'dépense', 0, 0, 0, 0),
	('مَثَل', 'proverbe', 0, 0, 0, 0),
	('أثر', 'vestige, monument', 0, 0, 0, 0),
	('إتفق على', 'convenir de', 0, 0, 0, 0),
	('أغلق', 'fermer', 0, 0, 0, 0),
	('مُتَوَفِّر', 'disponible, abondant', 0, 0, 0, 0),
	('دَلَّ على', 'indiquer', 0, 0, 0, 0),
	('مُعَاصِر', 'contemporain', 0, 0, 0, 0),
	('تفجير', 'attentat', 0, 0, 0, 0),
	('إعتداء', 'agression', 0, 0, 0, 0),
	('فات', 'échapper', 0, 0, 0, 0),
	('أعلن', 'déclarer, annoncer', 0, 0, 0, 0),
	('عَلاقَة', 'relation', 0, 0, 0, 0),
	('صار', 'devenir', 0, 0, 0, 0),
	('إستغرق', 'durer', 0, 0, 0, 0),
	('إقامة', 'séjour', 0, 0, 0, 0),
	('باع', 'vendre', 0, 0, 0, 0),
	('جُمْهور', 'foule', 0, 0, 0, 0),
	('أحسّ', 'ressentir', 0, 0, 0, 0),
	('تفادا', 'éviter', 0, 0, 0, 0),
	('أي', 'quel', 0, 0, 0, 0),
	('أيّة', 'quelle', 0, 0, 0, 0),
	('هجوم', 'attaque', 0, 0, 0, 0),
	('قُمَاش', 'tissu', 0, 0, 0, 0),
	('تتعلق', 'concerner, avoir trait à', 0, 0, 0, 0),
	('رعية', 'ressortissant', 0, 0, 0, 0),
	('لذيذ', 'agréable', 0, 0, 0, 0),
	('طبق', 'plat, assiette', 0, 0, 0, 0),
	('فاجأ', 'surprendre', 0, 0, 0, 0),
	('شاغِر', 'vacant, libre', 0, 0, 0, 0),
	('أهمل', 'négliger', 0, 0, 0, 0),
	('تَحِيَّة', 'salutation', 0, 0, 0, 0),
	('رئيس', 'chef', 0, 0, 0, 0),
	('رَئِيسيّ', 'principal', 0, 0, 0, 0),
	('عُطْلة', 'congé, chômage, vacances', 0, 0, 0, 0),
	('رُخْصَة القِيَادَة', 'permis de conduire', 0, 0, 0, 0),
	('مَساعٍ إدارية', 'démarches administratives', 0, 0, 0, 0),
	('حُبْلَى', 'enceinte', 0, 0, 0, 0),
	('أعجب', 'plaire', 0, 0, 0, 0),
	('آنستي', 'mademoiselle', 0, 0, 0, 0),
	('صباح', 'matin', 0, 0, 0, 0),
	('ردّ', 'répondre, répliquer', 0, 0, 0, 0),
	('نائب', 'député', 0, 0, 0, 0),
	('مظاهرة', 'manifestation', 0, 0, 0, 0),
	('جريح', 'blessé', 0, 0, 0, 0),
	('نشْرة إرصاديّة', 'bulletin météorologique', 0, 0, 0, 0),
	('قرأ', 'lire', 0, 0, 0, 0),
	('حسب ما سمعت', 'selon ce que j''ai entendu', 0, 0, 0, 0),
	('تربية', 'éducation', 0, 0, 0, 0),
	('خاصّة', 'en particulier, spécialement', 0, 0, 0, 0),
	('اِمْتِحَان', 'examen scolaire', 0, 0, 0, 0),
	('لا تنْس موعِدنا', 'n''oublie pas notre rendez-vous', 0, 0, 0, 0),
	('الذوق', 'le goût', 0, 0, 0, 0),
	('حُرّيّة', 'liberté', 0, 0, 0, 0),
	('خَيْل', 'chevaux (collectif)', 0, 0, 0, 0),
	('قُبّة', 'coupole, dôme', 0, 0, 0, 0),
	('فُرْصة', 'occasion', 0, 0, 0, 0),
	('تناقش', 'discuter', 0, 0, 0, 0),
	('حَدّ , حدود', 'frontière, limite', 0, 0, 0, 0),
	('إستطا ع', 'pouvoir', 0, 0, 0, 0),
	('ذاكرة', 'mémoire', 0, 0, 0, 0),
	('هنالك', 'là-bas', 0, 0, 0, 0),
	('مَوْعِد', 'rendez-vous, horaire, date', 0, 0, 0, 0),
	('ماء', 'eau', 0, 0, 0, 0),
	('هَؤُلَاءِ', 'ces', 0, 0, 0, 0),
	(' عَمَل', 'travail, œuvre', 0, 0, 0, 0),
	('في آن واحد', 'en même temps', 0, 0, 0, 0),
	('صيف', 'été', 0, 0, 0, 0),
	('نَجَّار', 'menuisier', 0, 0, 0, 0),
	('فجأةً', 0, 0, 0, 0, 0),
	('رجل أعمال', 'homme d''affaire', 0, 0, 0, 0),
	('جنّة', 'jardin, paradis', 0, 0, 0, 0),
	('مُتَوَاضِع', 'modeste', 0, 0, 0, 0),
	('حليب', 'lait', 0, 0, 0, 0),
	('حلب', 'Alep', 0, 0, 0, 0),
	('دمشق', 'Damas', 0, 0, 0, 0),
	('عبر', 'à travers', 0, 0, 0, 0),
	('غَرِيب', 'étrange, curieux, bizarre', 0, 0, 0, 0),
	('مَوضوع', 'sujet, thème', 0, 0, 0, 0),
	('بارِد', 'froid', 0, 0, 0, 0),
	('وَاجِب', 'devoir', 0, 0, 0, 0),
	('غيور', 'jaloux', 0, 0, 0, 0),
	('غرق', 'plonger, être submergé', 0, 0, 0, 0),
	('كفى', 'suffire', 0, 0, 0, 0),
	('هَدِيّة', 'cadeau', 0, 0, 0, 0),
	('قدّم', 'présenter', 0, 0, 0, 0),
	('سجّل', 'inscrire, enregistrer', 0, 0, 0, 0),
	('تَمّ', 'avoir lieu, s''accomplir', 0, 0, 0, 0),
	('قتيل', 'mort (victime)', 0, 0, 0, 0),
	('دقيقة', 'minute', 0, 0, 0, 0),
	('هُوَ الآخَرُ', 'lui aussi', 0, 0, 0, 0),
	('عشاء', 'dîner (nom)', 0, 0, 0, 0),
	('فَطِيرَة', 'tarte', 0, 0, 0, 0),
	('هاتف', 'téléphoner', 0, 0, 0, 0),
	('كنز', 'trésor caché', 0, 0, 0, 0),
	('شبعان', 'rassasié', 0, 0, 0, 0),
	('بطن', 'ventre', 0, 0, 0, 0),
	('سافر', 'voyager', 0, 0, 0, 0),
	('ساعد', 'aider à', 0, 0, 0, 0),
	('مُشْكِلَة', 'problème', 0, 0, 0, 0),
	('بالجِوار', 'dans les parages (voisinage)', 0, 0, 0, 0),
	('تخَلَّي عن', 'renoncer à', 0, 0, 0, 0),
	('صَاحِبُ', 'maître, propriétaire', 0, 0, 0, 0),
	('لحسن الحظ', 'par bonheur', 0, 0, 0, 0),
	('تَعَطَّل', 'tomber en panne', 0, 0, 0, 0),
	(' على حدةً', 'séparément', 0, 0, 0, 0),
	('حديثاً', 'récemment', 0, 0, 0, 0),
	('عُمْدَة', 'maire', 0, 0, 0, 0),
	('رَسْمِيّ', 'officiel', 0, 0, 0, 0),
	('أدب', 'politesse', 0, 0, 0, 0),
	('شديد', 'intense', 0, 0, 0, 0),
	('مَخافة أن', 'de crainte de, de crainte que', 0, 0, 0, 0),
	('إحتدم', 's''enflammer', 0, 0, 0, 0),
	('تحاور', 'dialoguer', 0, 0, 0, 0),
	('صافح', 'serrer la main', 0, 0, 0, 0),
	('مجموعة', 'ensemble, groupe', 0, 0, 0, 0),
	('شِجار', 'dispute', 0, 0, 0, 0),
	('إصْلاح', 'réparation', 0, 0, 0, 0),
	('إهْتِمام', 'préoccupation', 0, 0, 0, 0),
	('عَزِيز', 'cher … (affectueux)', 0, 0, 0, 0),
	('يُفَكِّرُ في', 'penser à', 0, 0, 0, 0),
	('حضّر', 'préparer', 0, 0, 0, 0),
	('لَم يَكُن', 'il n''y avait pas', 0, 0, 0, 0),
	('نَوْم', 'sieste', 0, 0, 0, 0),
	('هَاتِف جَوَال', 'téléphone portable', 0, 0, 0, 0),
	('حادث', 'accident, incident', 0, 0, 0, 0),
	('مطر', 'pluie', 0, 0, 0, 0),
	('تحادث', 'parler de, s''entretenir de', 0, 0, 0, 0),
	('قاعة', 'salle', 0, 0, 0, 0),
	('رئاسة', 'présidence', 0, 0, 0, 0),
	('بين', 'séparation, intervalle', 0, 0, 0, 0),
	('عيادة', 'consultation, cabinet, clinique', 0, 0, 0, 0),
	('رافق', 'accompagner', 0, 0, 0, 0),
	('ظهر', 'dos', 0, 0, 0, 0),
	('كُرَة القَدَم', 'football', 0, 0, 0, 0),
	('سُرْعة', 'vitesse, rapidité', 0, 0, 0, 0),
	('جمل', 'chameau', 0, 0, 0, 0),
	('وَرَقة', 'feuille, carte de jeu, billet', 0, 0, 0, 0),
	('مُتَقَاعِد', 'retraité', 0, 0, 0, 0),
	('لعب', 'jouer', 0, 0, 0, 0),
	('تأمين', 'assurance', 0, 0, 0, 0),
	('وَجْه ', 'visage', 0, 0, 0, 0),
	('حارّ', 'chaud', 0, 0, 0, 0),
	('قَبيح', 'laid', 0, 0, 0, 0),
	('صدر', 'paraître (publication)', 0, 0, 0, 0),
	('طريق', 'route, chemin, voie', 0, 0, 0, 0),
	('نهاية', 'fin, limite', 0, 0, 0, 0),
	('جَواز', 'passeport', 0, 0, 0, 0),
	('دار', 'tourner', 0, 0, 0, 0),
	('مُدَّة', 'durée, période', 0, 0, 0, 0),
	('مُسْتَقْبَل', 'futur, avenir', 0, 0, 0, 0),
	('نقص', 'manquer', 0, 0, 0, 0),
	('واجه', 'affronter, faire face à', 0, 0, 0, 0),
	('زوّد', 'fournir', 0, 0, 0, 0),
	('قسَّم', 'partager, diviser', 0, 0, 0, 0),
	('منح', 'remise d''un prix, octroi', 0, 0, 0, 0),
	('شَكْوى', 'plainte', 0, 0, 0, 0),
	('فَتاة', 'jeune fille', 0, 0, 0, 0),
	('درجة', 'degré (température, …)', 0, 0, 0, 0),
	('رُكْبة', 'genou', 0, 0, 0, 0),
	('وقت', 'quand, au moment où', 0, 0, 0, 0),
	('تحليل', 'analyse', 0, 0, 0, 0),
	('دَم', 'sang', 0, 0, 0, 0),
	('فحَص', 'examiner', 0, 0, 0, 0),
	('عنيف', 'violent', 0, 0, 0, 0),
	('عميق', 'profond', 0, 0, 0, 0),
	('تجوّل', 'se promener', 0, 0, 0, 0),
	('لازم', 'nécessaire', 0, 0, 0, 0),
	('حماية البيئة', 'protection de l''environnement', 0, 0, 0, 0),
	('مؤتمر', 'conférence, congrès', 0, 0, 0, 0),
	('قلق', 's''inquiéter', 0, 0, 0, 0),
	('حضور', 'présence', 0, 0, 0, 0),
	('ماهر', 'habile', 0, 0, 0, 0),
	('طازج', 'frais (fruit)', 0, 0, 0, 0),
	('مصروف', 'dépense', 0, 0, 0, 0),
	('سَيِّء', 'mauvais', 0, 0, 0, 0),
	('طارىء', 'urgences', 0, 0, 0, 0),
	('سِنّ', 'dent', 0, 0, 0, 0),
	('صيدلية', 'pharmacie', 0, 0, 0, 0),
	('حُقْنَة', 'injection', 0, 0, 0, 0),
	('إنذار', 'alerte', 0, 0, 0, 0),
	('قُنْبُلة', 'bombe', 0, 0, 0, 0),
	('خطر', 'danger', 0, 0, 0, 0),
	('واحة', 'oasis', 0, 0, 0, 0),
	('رماد', 'cendre', 0, 0, 0, 0),
	('طريق', 'route, chemin, voie', 0, 0, 0, 0),
	('رسم', 'dessin', 0, 0, 0, 0),
	('مَسْرَح', 'théâtre', 0, 0, 0, 0),
	('غادر', 'partir, quitter', 0, 0, 0, 0),
	('تدشين', 'inauguration', 0, 0, 0, 0),
	('قميص', 'chemise, tunique', 0, 0, 0, 0),
	('هدف', 'but', 0, 0, 0, 0),
	('تنظيم', 'organiser', 0, 0, 0, 0),
	('قُنْصُلِيّة', 'consulat', 0, 0, 0, 0),
	(' سَمَحَ', 'permettre', 0, 0, 0, 0),
	('مرحاض', 'toilettes', 0, 0, 0, 0),
	('ممرّ', 'couloir', 0, 0, 0, 0),
	('قريب', 'proche', 0, 0, 0, 0),
	('شمال', 'Nord', 0, 0, 0, 0),
	('جنوب', 'Sud', 0, 0, 0, 0),
	('شرق', 'Est', 0, 0, 0, 0),
	('غرب', 'Ouest', 0, 0, 0, 0),
	('أفضل', 'meilleur', 0, 0, 0, 0),
	('أزعج', 'déranger', 0, 0, 0, 0),
	('إقترح على', 'proposer à', 0, 0, 0, 0),
	('زواج', 'mariage', 0, 0, 0, 0),
	('مثّل', 'représenter', 0, 0, 0, 0),
	('مُوَزِّع آلِيّ', 'ditributeur automatique', 0, 0, 0, 0),
	('بيترا ', 'Pétra (Jordanie)', 0, 0, 0, 0),
	('صحراء', 'désert', 0, 0, 0, 0),
	('وِكالة', 'agence', 0, 0, 0, 0),
	('مـُمَثِّل', 'acteur, représentant', 0, 0, 0, 0),
	('مُرْشِد', 'guide', 0, 0, 0, 0),
	(' تعاقب', 'se succéder', 0, 0, 0, 0),
	('جدول', 'ruisseau, rivière', 0, 0, 0, 0),
	('تَنْمِية', 'développement', 0, 0, 0, 0),
	('كما', 'comme (+ verbe)', 0, 0, 0, 0),
	('مَعْلومات', 'information (s ?)', 0, 0, 0, 0),
	('مُرَتَّب', 'ordonné', 0, 0, 0, 0),
	('ضَيْف', 'invité', 0, 0, 0, 0),
	('غرفة', 'pièce, salle', 0, 0, 0, 0),
	('وضع', 'poser, mettre, laisser', 0, 0, 0, 0),
	('فنّ', 'art', 0, 0, 0, 0),
	('حكومة', 'gouvernement', 0, 0, 0, 0),
	('تقريبيًّا', 'environ', 0, 0, 0, 0),
	('سكن', 'habiter', 0, 0, 0, 0),
	('الشرق الأدنى', 'le Proche-Orient', 0, 0, 0, 0),
	('فقير', 'pauvre', 0, 0, 0, 0),
	('الْشَّرْق الْأَوْسَط', 'le Moyen-Orient', 0, 0, 0, 0),
	('بطالة', 'chômage', 0, 0, 0, 0),
	('صنعاء', 'Sanaa (capitale du Yémen)', 0, 0, 0, 0),
	('رغما', 'malgré', 0, 0, 0, 0),
	('مِتْحَف', 'musée', 0, 0, 0, 0),
	('رأى', 'voir', 0, 0, 0, 0),
	('عيد ميلاد', 'anniversaire', 0, 0, 0, 0),
	('زوج', 'mari', 0, 0, 0, 0),
	('إمرأة', 'femme', 0, 0, 0, 0),
	('القاهرة', 'Le Caire', 0, 0, 0, 0),
	('قَد', 'peut-être', 0, 0, 0, 0),
	('ذَكِيّ', 'intelligent', 0, 0, 0, 0),
	('تماما', 'parfaitement', 0, 0, 0, 0),
	('بحر', 'mer', 0, 0, 0, 0),
	('حصل', 'obtenir, acquérir', 0, 0, 0, 0),
	('تجارة', 'commerce', 0, 0, 0, 0),
	('كيس', 'sac', 0, 0, 0, 0),
	('بمُنَاسَبَة', 'à l''occasion de', 0, 0, 0, 0),
	('تَابِل', 'épice', 0, 0, 0, 0),
	('عمّ', 'oncle (côté paternel)', 0, 0, 0, 0),
	('شهادة', 'diplôme', 0, 0, 0, 0),
	('منسيج / قُماش', 'tissu', 0, 0, 0, 0),
	('عائلة', 'famille', 0, 0, 0, 0),
	(' دار', 'maison', 0, 0, 0, 0),
	('سبح', 'nager', 0, 0, 0, 0),
	('حَكِيم', 'sage', 0, 0, 0, 0),
	('طفل', 'enfant', 0, 0, 0, 0),
	('بقرة', 'vache', 0, 0, 0, 0),
	('غني', 'riche', 0, 0, 0, 0),
	('حديث', 'moderne', 0, 0, 0, 0),
	('دِولة', 'Etat (nation)', 0, 0, 0, 0),
	('فاخِر', 'luxueux, de luxe', 0, 0, 0, 0),
	('قدّم نفسه', 'se présenter', 0, 0, 0, 0),
	('سنّ', 'âge', 0, 0, 0, 0),
	('صلاة', 'prière', 0, 0, 0, 0),
	('أخت', 'sœur', 0, 0, 0, 0),
	('درس', 'étudier', 0, 0, 0, 0),
	('درّس', 'enseigner', 0, 0, 0, 0),
	('حقّ', 'droit', 0, 0, 0, 0),
	('قرية', 'village', 0, 0, 0, 0),
	('عمل', 'faire, travailler', 0, 0, 0, 0),
	('جامعة', 'université', 0, 0, 0, 0),
	('زهرة', 'fleur', 0, 0, 0, 0),
	('ثمرة', 'fruit', 0, 0, 0, 0),
	('إنّ … لـ … !', 'vraiment !', 0, 0, 0, 0),
	('بالتّالي', 'de ce fait', 0, 0, 0, 0),
	('تناول', 'prise de', 0, 0, 0, 0),
	('عادَل', 'équivaloir à', 0, 0, 0, 0),
	('كان + inaccompli', 'formation de l''imparfait', 0, 0, 0, 0),
	('كان قد + accompli', 'formation du plus-que-parfait', 0, 0, 0, 0),
	('لنْ + sujonctif', 'négation du futur', 0, 0, 0, 0),
	('صعود', 'montée', 0, 0, 0, 0),
	('تَسَتَّرَ', 'se cacher', 0, 0, 0, 0),
	('هل يُرْضِيك ?', 'Cela te convient ?', 0, 0, 0, 0),
	('مُكْتَظّ (بــ)', 'plein (de)', 0, 0, 0, 0),
	('دعا', 'appeler', 0, 0, 0, 0),
	('مُمْتِع', 'agréable', 0, 0, 0, 0),
	('غير (+ indicatif)', 'négation d''un adjectif', 0, 0, 0, 0),
	('فِراش', 'lit', 0, 0, 0, 0),
	('ناول', 'donner', 0, 0, 0, 0),
	('لَوْ … لَــ … ', 'conditionnel passé irréel', 0, 0, 0, 0),
	('إخْتِراق', 'traversée', 0, 0, 0, 0),
	('إذ أنّ', 'puisque', 0, 0, 0, 0),
	('مُهِمّ', 'intéressant', 0, 0, 0, 0),
	('لا + apocopé', 'expression de la défense', 0, 0, 0, 0),
	('كــــــــ', 'comme (+ nom ou démonstratif)', 0, 0, 0, 0),
	('لا بدّ لي … إلّا', 'il me faut absolument (pas d''issue pour moi)', 0, 0, 0, 0),
	('لا بأْسَ بِهِ', 'il n''est pas mal', 0, 0, 0, 0),
	('لَم + apocopé + بعد', 'ne pas … encore', 0, 0, 0, 0),
	('مَثَلاً', 'par exemple', 0, 0, 0, 0),
	('حول + indicatif', 'autour de', 0, 0, 0, 0),
	('آن', 'moment', 0, 0, 0, 0),
	('قيلَ لي … ', 'on m''a dit', 0, 0, 0, 0),
	('ألوَيْل لك !', 'malheur à toi !', 0, 0, 0, 0),
	('مَوجُود', 'existant', 0, 0, 0, 0),
	('قِف هنا !', 'arrête-toi ici !', 0, 0, 0, 0),
	('مُتَوَجِّه إلى … ', 'se dirigeant vers', 0, 0, 0, 0),
	('كم يُساوي … ?', 'combien coûte … ? (max)', 0, 0, 0, 0),
	('ألغَوث !', 'Au secours !', 0, 0, 0, 0),
	('إبْرة', 'piqûre, épingle', 0, 0, 0, 0),
	('مُثير للإهْتِمام', 'intéressant, suscitant l''intérêt', 0, 0, 0, 0),
	('إنصرف', 's''en aller', 0, 0, 0, 0),
	('شاىب', 'homme d''âge mûr, vieux, aux cheveux blancs', 0, 0, 0, 0),
	('ذاتَ يومٍ', 'un certain jour', 0, 0, 0, 0),
	('إشعاعيّ', 'radio-actif', 0, 0, 0, 0),
	('طُمانينة', 'sérénité', 0, 0, 0, 0);



/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;