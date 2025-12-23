-- ========================================
-- Script création bases/utilisateurs MySQL
-- Exécuter : mysql -u dba -p < creation.sql
-- ========================================

-- Création des 4 bases de données
CREATE DATABASE IF NOT EXISTS robot1;
CREATE DATABASE IF NOT EXISTS robot2;
CREATE DATABASE IF NOT EXISTS robot3;
CREATE DATABASE IF NOT EXISTS robot4;

-- Création des 4 utilisateurs robotX (accès TOTAL à leur base)
CREATE USER IF NOT EXISTS 'robot1'@'localhost' IDENTIFIED BY 'robot1pass';
GRANT ALL PRIVILEGES ON robot1.* TO 'robot1'@'localhost';

CREATE USER IF NOT EXISTS 'robot2'@'localhost' IDENTIFIED BY 'robot2pass';
GRANT ALL PRIVILEGES ON robot2.* TO 'robot2'@'localhost';

CREATE USER IF NOT EXISTS 'robot3'@'localhost' IDENTIFIED BY 'robot3pass';
GRANT ALL PRIVILEGES ON robot3.* TO 'robot3'@'localhost';

CREATE USER IF NOT EXISTS 'robot4'@'localhost' IDENTIFIED BY 'robot4pass';
GRANT ALL PRIVILEGES ON robot4.* TO 'robot4'@'localhost';

-- Utilisateur grafana_reader (SELECT sur TOUTES les tables des 4 bases)
CREATE USER IF NOT EXISTS 'grafana_reader'@'localhost' IDENTIFIED BY 'GRAFpass123';
GRANT SELECT ON robot1.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON robot2.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON robot3.* TO 'grafana_reader'@'localhost';
GRANT SELECT ON robot4.* TO 'grafana_reader'@'localhost';

-- Appliquer les privilèges
FLUSH PRIVILEGES;

-- Création table MESURES dans robot1
USE robot1;

CREATE TABLE IF NOT EXISTS mesures (
    mesure_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL COMMENT 'Fourni par l''application',
    cle VARCHAR(50) NOT NULL COMMENT 'Ex: temperature, humidite, pression',
    valeur FLOAT NOT NULL COMMENT 'Valeur mesurée',
    INDEX idx_timestamp (timestamp),
    INDEX idx_cle (cle),
    INDEX idx_timestamp_cle (timestamp, cle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Vérification finale (optionnel)
SHOW DATABASES LIKE 'robot%';
SELECT User, Host FROM mysql.user WHERE User LIKE 'robot%' OR User = 'grafana_reader';
USE robot1; DESCRIBE mesures;

-- Fin du script
