-- ========================================
-- Script création table events
-- Stocke les événements MQTT du robot
-- Format attendu : {"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
-- Exécuter : mysql -u robot3 -probot3pass robot3 < creation_events.sql
-- ========================================

CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL COMMENT 'Horodatage de l''événement (converti depuis epoch)',
    event_type VARCHAR(50) NOT NULL COMMENT 'Type : color_done, color_error, etc.',
    color VARCHAR(20) DEFAULT NULL COMMENT 'Couleur demandée',
    status VARCHAR(20) DEFAULT NULL COMMENT 'Résultat : success, error, etc.',
    raw_json TEXT NOT NULL COMMENT 'Message JSON brut reçu via MQTT',
    INDEX idx_timestamp (timestamp),
    INDEX idx_event_type (event_type),
    INDEX idx_timestamp_event (timestamp, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
