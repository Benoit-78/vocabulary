
-- If localhost
CREATE DATABASE wh0_Are_y0u_portuguese;
USE wh0_Are_y0u_portuguese;



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
    `foreign` CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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
    `foreign` CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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
    portugues CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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



INSERT INTO `version_voc` (`portugues`, `français`, `creation_date`, `nb`, `score`) VALUES
    ('branco', 'blanc', '2024-01-01', 15, 0),
    ('maduro', 'mûr', '2024-01-01', 5, 0),
    ('a praia', 'la plage', '2024-01-01', 7, 0),
    ('o sorvete', 'le sorbet', '2024-01-01', 6, 0),
    ('gelado', 'glacé', '2024-01-01', 5, 0),
    ('escuro', 'obscur', '2024-01-01', 8, 0),
    ('a floresta', 'la forêt', '2024-01-01', 7, 0),
    ('a comida', 'la nourriture', '2024-01-01', 9, 0),
    ('o vizinho', 'le voisin', '2024-01-01', 8, 0),
    ('o espelho', 'le miroir', '2024-01-01', 4, 0),
    ('a sala', 'le salon', '2024-01-01', 6, 0),
    ('a moeda nacional', 'la monnaie nationale', '2024-01-01', 6, 0),
    ('o dinheiro', 'l’argent', '2024-01-01', 6, 0),
    ('perto', 'près', '2024-01-01', 7, 0),
    ('o quarteirão', 'le pâté de maisons', '2024-01-01', 12, 0),
    ('o irmão', 'le frère', '2024-01-01', 6, 0),
    ('o trem', 'le train', '2024-01-01', 8, 0),
    ('em ponto', 'ponctuellement, pile', '2024-01-01', 5, 0),
    ('o prazer', 'le plaisir', '2024-01-01', 5, 0),
    ('a canção', 'la chanson', '2024-01-01', 7, 0),
    ('o ingresso', 'le billet', '2024-01-01', 6, 0),
    ('o jogo', 'le jeu', '2024-01-01', 9, 0),
    ('o time', 'l’équipe (de foot)', '2024-01-01', 6, 0),
    ('Parece que ...', 'Il semble que …', '2024-01-01', 6, 0),
    ('a certeza', 'la certitude', '2024-01-01', 6, 0),
    ('Não atende', 'Ca ne répond pas', '2024-01-01', 7, 0),
    ('esperar', 'attendre', '2024-01-01', 7, 0),
    ('resolver', 'résoudre', '2024-01-01', 6, 0),
    ('sinto', 'je regrette', '2024-01-01', 9, 0),
    ('a manhã', 'le matin', '2024-01-01', 4, 0),
    ('avisar', 'prévenir', '2024-01-01', 10, 0),
    ('até logo', 'à bientôt', '2024-01-01', 6, 0),
    ('a lua', 'la lune', '2024-01-01', 7, 0),
    ('a tarde', 'l’après-midi', '2024-01-01', 8, 0),
    ('perguntar', 'demander', '2024-01-01', 6, 0),
    ('a balconista', 'la vendeuse', '2024-01-01', 9, 0),
    ('o arroz', 'le riz', '2024-01-01', 7, 0),
    ('o feijão', 'le haricot', '2024-01-01', 3, 0),
    ('desligado', 'distrait (délié)', '2024-01-01', 8, 0),
    ('a recado', 'le message', '2024-01-01', 4, 0),
    ('cedo', 'tôt', '2024-01-01', 8, 0),
    ('atrasado', 'en retard', '2024-01-01', 6, 0),
    ('o sorte', 'la chance', '2024-01-01', 9, 0),
    ('o avô', 'le grand-père', '2024-01-01', 6, 0),
    ('o rolo', 'le rouleau', '2024-01-01', 6, 0),
    ('a palha', 'la paille', '2024-01-01', 5, 0),
    ('acho', 'je trouve', '2024-01-01', 10, 0),
    ('ruim', 'mauvais', '2024-01-01', 5, 0),
    ('o cheiro', 'l’odeur', '2024-01-01', 6, 0),
    ('demoro', 'je m’attarde', '2024-01-01', 8, 0),
    ('a medida', 'la mesure', '2024-01-01', 7, 0),
    ('a colher', 'la cuiller', '2024-01-01', 7, 0),
    ('o gelo', 'la glace', '2024-01-01', 7, 0),
    ('beber', 'boire', '2024-01-01', 5, 0),
    ('Cuidado !', 'Attention !', '2024-01-01', 7, 0),
    ('a saúde', 'la santé', '2024-01-01', 5, 0),
    ('tomar', 'prendre', '2024-01-01', 9, 0),
    ('último', 'dernier', '2024-01-01', 6, 0),
    ('pequeno', 'petit', '2024-01-01', 7, 0),
    ('a côr', 'la couleur', '2024-01-01', 4, 0),
    ('levar', 'emporter', '2024-01-01', 11, 0),
    ('sair', 'sortir', '2024-01-01', 6, 0),
    ('lotado', 'bondé', '2024-01-01', 7, 0),
    ('o lugar', 'l’endroit', '2024-01-01', 10, 0),
    ('sentar', 'asseoir', '2024-01-01', 5, 0),
    ('ficar', 'rester', '2024-01-01', 6, 0),
    ('carregar', 'porter', '2024-01-01', 7, 0),
    ('a cabeça', 'la tête', '2024-01-01', 3, 0),
    ('esqueço', 'j’oublie', '2024-01-01', 9, 0),
    ('frio', 'frais, froid', '2024-01-01', 5, 0),
    ('o paletó', 'la veste', '2024-01-01', 11, 0),
    ('lã', 'la laine', '2024-01-01', 7, 0),
    ('estranho', 'étrange', '2024-01-01', 5, 0),
    ('por acaso', 'par hasard', '2024-01-01', 6, 0),
    ('aí', 'là', '2024-01-01', 5, 0),
    ('cheio de …', 'plein de …', '2024-01-01', 6, 0),
    ('preciso', 'j’ai besoin', '2024-01-01', 9, 0),
    ('apanhá', 'chercher', '2024-01-01', 8, 0),
    ('pronto', 'prêt', '2024-01-01', 6, 0),
    ('depois', 'après', '2024-01-01', 7, 0),
    ('divirta', 'se distraire', '2024-01-01', 6, 0),
    ('felizmente', 'heureusement', '2024-01-01', 7, 0),
    ('ainda', 'encore', '2024-01-01', 7, 0),
    ('a platéia', 'l’orchestre', '2024-01-01', 5, 0),
    ('a gente fina', 'le gratin', '2024-01-01', 8, 0),
    ('a almofada', 'le coussin', '2024-01-01', 6, 0),
    ('o chão', 'le sol', '2024-01-01', 5, 0),
    ('a feira', 'le marché', '2024-01-01', 7, 0),
    ('peixe', 'du poisson', '2024-01-01', 8, 0),
    ('hortelã', 'la menthe', '2024-01-01', 5, 0),
    ('o costume', 'l’habitude', '2024-01-01', 8, 0),
    ('a maçã', 'la pomme', '2024-01-01', 9, 0),
    ('a abacaxi', 'l’ananas', '2024-01-01', 8, 0),
    ('a laranja', 'l’orange', '2024-01-01', 6, 0),
    ('o carro', 'la voiture', '2024-01-01', 5, 0),
    ('o semáforo', 'le feu de circulation', '2024-01-01', 6, 0),
    ('peço', 'je demande', '2024-01-01', 9, 0),
    ('o algodão', 'le coton', '2024-01-01', 5, 0),
    ('a limpeza', 'le nettoyage', '2024-01-01', 11, 0),
    ('em voz baixa', 'à voix basse', '2024-01-01', 5, 0),
    ('odeio', 'je déteste', '2024-01-01', 5, 0),
    ('sozinho', 'seul', '2024-01-01', 3, 0),
    ('o peso', 'le poids', '2024-01-01', 2, 0),
    ('doí', 'ça fait mal', '2024-01-01', 3, 0),
    ('pagar', 'payer', '2024-01-01', 2, 0),
    ('o imposto', 'l’impôt', '2024-01-01', 5, 0),
    ('o aluguei', 'le loyer', '2024-01-01', 7, 0),
    ('a licença', 'l’autorisation', '2024-01-01', 3, 0),
    ('Pois não', 'Mais certainement', '2024-01-01', 4, 0),
    ('a dôr', 'la douleur', '2024-01-01', 3, 0),
    ('o pescoço', 'le cou', '2024-01-01', 4, 0),
    ('aborrecido', 'ennuyé, embêté', '2024-01-01', 2, 0),
    ('o jeito', 'la façon, la manière', '2024-01-01', 6, 0),
    ('amanhã', 'demain', '2024-01-01', 2, 0),
    ('voltar', 'retourner, revenir', '2024-01-01', 3, 0),
    ('providenciar', 'préparer', '2024-01-01', 3, 0),
    ('assim', 'ainsi', '2024-01-01', 4, 0),
    ('o nome', 'le nom', '2024-01-01', 4, 0),
    ('geralmente', 'généralement', '2024-01-01', 5, 0),
    ('Fica combinado', 'C’est d’accord', '2024-01-01', 4, 0),
    ('nada', 'rien', '2024-01-01', 5, 0),
    ('o passeio', 'la promenade', '2024-01-01', 1, 0),
    ('dar', 'donner', '2024-01-01', 5, 0),
    ('as crianças', 'les enfants', '2024-01-01', 2, 0),
    ('vir', 'venir', '2024-01-01', 4, 0),
    ('a roupa', 'le linge', '2024-01-01', 4, 0),
    ('a noite', 'la nuit', '2024-01-01', 8, 0),
    ('a folga', 'le congé', '2024-01-01', 1, 0),
    ('buscar', 'chercher', '2024-01-01', 6, 0),
    ('dentro', 'à l’intérieur', '2024-01-01', 0, 0),
    ('a afilhada', 'la filleule', '2024-01-01', 3, 0),
    ('receber', 'recevoir', '2024-01-01', 3, 0),
    ('chore', 'pleurer', '2024-01-01', 2, 0),
    ('Eu não ligo para …', 'Je ne m’intéresse pas à …', '2024-01-01', 5, 0),
    ('o cavalo', 'le cheval', '2024-01-01', 3, 0),
    ('o bicho', 'l’animal', '2024-01-01', 2, 0),
    ('a padaria', 'la boulangerie', '2024-01-01', 4, 0),
    ('a chuva', 'la pluie', '2024-01-01', 2, 0),
    ('a moçada', 'les jeunes gens', '2024-01-01', 7, 0),
    ('a bofetada', 'la gifle', '2024-01-01', 1, 0),
    ('gostar de', 'aimer, apprécier', '2024-01-01', 5, 0),
    ('a viagem', 'le voyage', '2024-01-01', 1, 0),
    ('o roteiro', 'l’itinéraire', '2024-01-01', 1, 0),
    ('descansar', 'se reposer', '2024-01-01', 2, 0),
    ('um pouquinho', 'un petit peu', '2024-01-01', 2, 0),
    ('conhecer', 'connaître', '2024-01-01', 3, 0),
    ('estrangeiro', 'étranger', '2024-01-01', 3, 0),
    ('se hospedar', 'se loger', '2024-01-01', 3, 0),
    ('barato', 'bon marché', '2024-01-01', 2, 0),
    ('o serviço', 'le travail, l’activité professionnelle', '2024-01-01', 0, 0),
    ('o navio', 'le bateau', '2024-01-01', 2, 0),
    ('agradável', 'agréable', '2024-01-01', 1, 0),
    ('o calor', 'la chaleur', '2024-01-01', 2, 0),
    ('o meio', 'le milieu', '2024-01-01', 2, 0),
    ('a vela', 'la bougie', '2024-01-01', 4, 0),
    ('a rainha', 'la reine', '2024-01-01', 2, 0),
    ('cada um', 'chacun', '2024-01-01', 2, 0),
    ('rezar', 'prier', '2024-01-01', 0, 0),
    ('jogar', 'lancer', '2024-01-01', 1, 0),
    ('seguinte (adj.)', 'suivant', '2024-01-01', 1, 0),
    ('a crença', 'la croyance', '2024-01-01', 1, 0),
    ('a camada', 'la couche', '2024-01-01', 4, 0),
    ('acender', 'allumer', '2024-01-01', 1, 0),
    ('ao vivo', 'en direct', '2024-01-01', 1, 0),
    ('a loja', 'le magasin, la boutique', '2024-01-01', 1, 0),
    ('ontem', 'hier', '2024-01-01', 1, 0),
    ('o cartão de credito', 'la carte de crédit', '2024-01-01', 1, 0),
    ('provável', 'probable', '2024-01-01', 0, 0),
    ('a meia', 'la chaussette', '2024-01-01', 3, 0),
    ('o presente', 'le cadeau', '2024-01-01', 0, 0),
    ('o conjunto', 'l’ensemble', '2024-01-01', 0, 0),
    ('o casamento', 'le mariage', '2024-01-01', 1, 0),
    ('possível', 'possible', '2024-01-01', 1, 0),
    ('a coluna social', 'le carnet mondain', '2024-01-01', 1, 0),
    ('se chamar', 's’appeler', '2024-01-01', 1, 0),
    ('os noivos', 'les fiancés', '2024-01-01', 0, 0),
    ('os casados', 'les mariés', '2024-01-01', 0, 0),
    ('o carinho', 'la tendresse', '2024-01-01', 0, 0),
    ('arrumar', 'ranger / se trouver', '2024-01-01', 0, 0),
    ('trocar', 'échanger', '2024-01-01', 0, 0),
    ('a flôr', 'la fleur', '2024-01-01', 1, 0),
    ('brigar', 'se battre, se disputer', '2024-01-01', 1, 0),
    ('um amor de Carnaval', 'un béguin', '2024-01-01', 1, 0),
    ('fora', 'à l’extérieur', '2024-01-01', 1, 0),
    ('o calçado', 'la chaussure', '2024-01-01', 1, 0),
    ('a drogaria', 'la pharmacie', '2024-01-01', 0, 0),
    ('o pedreiro', 'le maçon', '2024-01-01', 0, 0),
    ('o subúrbio', 'la banlieue', '2024-01-01', 0, 0),
    ('o mês', 'le mois', '2024-01-01', 0, 0),
    ('a ponte', 'le pont', '2024-01-01', 1, 0),
    ('a rodoviária', 'la gare routière', '2024-01-01', 1, 0),
    ('convidar', 'inviter', '2024-01-01', 1, 0),
    ('à esquerda', 'à gauche', '2024-01-01', 1, 0),
    ('gritar', 'crier', '2024-01-01', 1, 0),
    ('alguém', 'quelqu’un', '2024-01-01', 0, 0),
    ('retratar', 'photographier', '2024-01-01', 0, 0),
    ('a sabia', 'une espère d’oiseau très populaire du Brésil', '2024-01-01', 0, 0),
    ('a mão', 'la main', '2024-01-01', 0, 0),
    ('pular', 'plonger', '2024-01-01', 0, 0),
    ('escutar', 'écouter', '2024-01-01', 1, 0),
    ('agora', 'maintenant', '2024-01-01', 1, 0),
    ('parar', 's’arrêter', '2024-01-01', 1, 0),
    ('o braço', 'le bras', '2024-01-01', 1, 0),
    ('a praça', 'la place (en ville)', '2024-01-01', 0, 0),
    ('andar', 'marcher', '2024-01-01', 0, 0),
    ('reto', 'tout droit', '2024-01-01', 0, 0),
    ('então', 'alors', '2024-01-01', 0, 0),
    ('do lado de lá', 'de l’autre côté', '2024-01-01', 0, 0),
    ('a calçada', 'le trottoir', '2024-01-01', 1, 0),
    ('ali', 'là-bas', '2024-01-01', 1, 0),
    ('a esquina', 'le coin', '2024-01-01', 1, 0),
    ('o prédio', 'l’immeuble', '2024-01-01', 1, 0),
    ('a andar', 'l’étage', '2024-01-01', 0, 0),
    ('o fim de semana', 'le week-end', '2024-01-01', 0, 0),
    ('a media', ' la moyenne', '2024-01-01', 0, 0),
    ('um jovem', 'un jeune', '2024-01-01', 0, 0),
    ('a alegria', 'la joie', '2024-01-01', 0, 0),
    ('deixar', 'laisser', '2024-01-01', 0, 0),
    ('acabar', 'terminer, finir', '2024-01-01', 0, 0),
    ('bastante', 'suffisamment', '2024-01-01', 0, 0),
    ('os talheres', 'les couverts (d’une table)', '2024-01-01', 0, 0),
    ('o prato', 'l’assiette', '2024-01-01', 0, 0),
    ('o condomínio', 'les charges locatives', '2024-01-01', 0, 0),
    ('aprontar', 'préparer', '2024-01-01', 0, 0),
    ('o coragem', 'le courage', '2024-01-01', 0, 0),
    ('o cunhado', 'le beau-frère', '2024-01-01', 0, 0),
    ('apesar', 'malgré', '2024-01-01', 0, 0),
    ('a idade', 'l’âge', '2024-01-01', 0, 0),
    ('a verdade', 'la vérité', '2024-01-01', 0, 0),
    ('maravilho', 'merveilleux', '2024-01-01', 0, 0),
    ('a mulher', 'la femme', '2024-01-01', 0, 0),
    ('o direito', 'le droit', '2024-01-01', 0, 0),
    ('desafinado', 'désaccordé, faux (musique)', '2024-01-01', 0, 0),
    ('aficionado', 'adepte, fan / affectueux', '2024-01-01', 0, 0),
    ('por outro lado', 'd’un autre côté', '2024-01-01', 0, 0),
    ('bascamente', 'essentiellement', '2024-01-01', 0, 0),
    ('a mudança', 'le changement', '2024-01-01', 0, 0),
    ('queimadas', 'brûlé', '2024-01-01', 0, 0),
    ('pegando', 'contagieux', '2024-01-01', 0, 0),
    ('o estrago', 'le dommage', '2024-01-01', 0, 0),
    ('da certo', 'ça marche', '2024-01-01', 0, 0),
    ('a pesquisa', 'la recherche', '2024-01-01', 0, 0),
    ('a poeira', 'la poussière', '2024-01-01', 0, 0),
    ('a rajada', 'la rafale', '2024-01-01', 0, 0),
    ('o granizo', 'la grêle', '2024-01-01', 0, 0),
    ('o bafado', 'le souffle', '2024-01-01', 0, 0),
    ('os raios (?)', 'les rayons / l’ensoleillement', '2024-01-01', 0, 0),
    ('os fomento', 'la promotion', '2024-01-01', 0, 0),
    ('fechado', 'fermé', '2024-01-01', 0, 0),
    ('amarelo', 'jaune', '2024-01-01', 0, 0),
    ('a senha', 'le mot de passe', '2024-01-01', 0, 0),
    ('a ameaça', 'la menace', '2024-01-01', 0, 0),
    ('a abordagem', 'l’approche', '2024-01-01', 0, 0),
    ('levemente', 'légèrement', '2024-01-01', 0, 0),
    ('o gráfico de pizza', 'le diagramme camembert', '2024-01-01', 0, 0),
    ('apenas', 'seulement', '2024-01-01', 0, 0),
    ('a amostra', 'l’échantillon, l’exemple', '2024-01-01', 0, 0),
    ('próxima', 'suivant', '2024-01-01', 0, 0),
    ('limpar', 'nettoyer, effacer', '2024-01-01', 0, 0),
    ('a trovoada', 'l’orage', '2024-01-01', 0, 0),
    ('a qualquer hora', 'à toute heure', '2024-01-01', 0, 0),
    ('esquecido', 'oublié', '2024-01-01', 0, 0),
    ('o cargo de liderança', 'la position de leader', '2024-01-01', 0, 0),
    ('pancadas', 'des vents forts', '2024-01-01', 0, 0),
    ('enchente', 'l’inondation', '2024-01-01', 0, 0),
    ('espalhar', 'se propager', '2024-01-01', 0, 0),
    ('alagar', 'inonder', '2024-01-01', 0, 0),
    ('nadar', 'nager', '2024-01-01', 0, 0),
    ('a janela', 'la fenêtre', '2024-01-01', 0, 0),
    ('na tela', 'sur l’écran', '2024-01-01', 0, 0),
    ('aluguel (common name)', 'la location', '2024-01-01', 0, 0),
    ('a lenda', 'la légende', '2024-01-01', 0, 0),
    ('o superavit', 'un surplus, un excédent', '2024-01-01', 0, 0),
    ('o desempenho', 'la performance', '2024-01-01', 0, 0),
    ('o morador', 'le résident', '2024-01-01', 0, 0),
    ('roupas', 'vêtements / prêt-à-porter', '2024-01-01', 0, 0),
    ('dentre outros', 'entre autres', '2024-01-01', 0, 0),
    ('entrei em contato com', 'Je suis entré en contact avec', '2024-01-01', 0, 0);
