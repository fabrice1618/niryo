# Tests MQTT Message Handler

Ce document décrit les tests à exécuter sur le NUC pour valider l'implémentation.

## Prérequis

1. **Configuration**: Fichier `.env` configuré avec les paramètres du NUC
2. **Services actifs**:
   - Mosquitto (MQTT broker) en cours d'exécution
   - MySQL en cours d'exécution avec la base `robot1` créée
3. **Dépendances Python**: `pip install -r requirements.txt`

## Structure des tests

| Script | Description | Prérequis |
|--------|-------------|-----------|
| `test_mqtt_connection.py` | Test de connexion au broker MQTT | Mosquitto actif |
| `test_mysql_connection.py` | Test de connexion à MySQL et structure de table | MySQL actif, table `mesures` créée |
| `test_validation.py` | Test de validation des messages | Mosquitto + `subscriber.py` en cours |
| `test_integration.py` | Test d'intégration complet MQTT → MySQL | Tous services + `subscriber.py` en cours |
| `run_all_tests.sh` | Script bash pour exécuter tous les tests | Tous les prérequis |

## Exécution rapide

### Méthode 1: Script automatique

```bash
cd code/mqtt_message
chmod +x run_all_tests.sh
./run_all_tests.sh
```

Le script vous guidera et demandera confirmation pour les tests nécessitant `subscriber.py`.

### Méthode 2: Tests individuels

```bash
# Test 1: Connexion MQTT
python3 test_mqtt_connection.py

# Test 2: Connexion MySQL
python3 test_mysql_connection.py

# Test 3: Validation (démarrer subscriber.py d'abord)
# Terminal 1:
python3 subscriber.py

# Terminal 2:
python3 test_validation.py

# Test 4: Intégration (démarrer subscriber.py d'abord)
# Terminal 1:
python3 subscriber.py

# Terminal 2:
python3 test_integration.py
```

## Description détaillée des tests

### Test 1: MQTT Connection (`test_mqtt_connection.py`)

**Objectif**: Vérifier la connectivité au broker MQTT avec authentification

**Ce qui est testé**:
- Connexion au broker avec les identifiants du `.env`
- Souscription au topic `exemple/capteur`
- Authentification correcte

**Résultat attendu**:
```
✓ Connection successful
✓ Subscription successful to topic: exemple/capteur
✅ PASSED: MQTT connection test
```

**En cas d'échec**:
- Vérifier que Mosquitto est actif: `sudo systemctl status mosquitto`
- Vérifier l'adresse IP et le port dans `.env`
- Vérifier les credentials MQTT

---

### Test 2: MySQL Connection (`test_mysql_connection.py`)

**Objectif**: Vérifier la connectivité MySQL et la structure de la table

**Ce qui est testé**:
- Connexion à la base de données
- Existence de la table `mesures`
- Structure de la table (colonnes: `mesure_id`, `timestamp`, `cle`, `valeur`)
- Permissions d'écriture

**Résultat attendu**:
```
✓ Connection successful
✓ Table 'mesures' exists
✓ Write permission OK
✅ PASSED: MySQL connection test
```

**En cas d'échec**:
- Vérifier que MySQL est actif: `sudo systemctl status mysql`
- Vérifier que la base `robot1` existe
- Exécuter `/database/creation.sql` si la table n'existe pas
- Vérifier les credentials MySQL dans `.env`

---

### Test 3: Message Validation (`test_validation.py`)

**Objectif**: Tester la validation des messages par le subscriber

**Prérequis**: `subscriber.py` doit être en cours d'exécution

**Ce qui est testé**:
1. Message valide (accepté)
2. JSON invalide (warning attendu)
3. Clés manquantes (warning attendu)
4. Température hors plage (warning attendu)
5. Humidité hors plage (warning attendu)
6. Pression hors plage (warning attendu)
7. Format timestamp invalide (warning attendu)
8. Valeurs aux limites (acceptées)

**Résultat attendu**:
- Le test publie 10 messages de test
- Consulter les logs de `subscriber.py` pour vérifier les warnings

**Messages de validation attendus dans subscriber.py**:
```
[TIMESTAMP] WARNING JSON invalide ignoré: ...
[TIMESTAMP] WARNING Clé manquante ignorée: timestamp
[TIMESTAMP] WARNING Valeur hors plage ignorée: temperature=150.0
[TIMESTAMP] WARNING Valeur hors plage ignorée: humidite=150.0
[TIMESTAMP] WARNING Valeur hors plage ignorée: pression=1200.0
[TIMESTAMP] WARNING Format timestamp invalide: ...
[TIMESTAMP] INFO Message reçu et traité: 3 mesures insérées (x3 pour les valides)
```

---

### Test 4: Integration (`test_integration.py`)

**Objectif**: Test d'intégration complet end-to-end

**Prérequis**: `subscriber.py` doit être en cours d'exécution

**Ce qui est testé**:
1. Publication d'un message de test via MQTT
2. Attente du traitement par `subscriber.py`
3. Vérification dans MySQL que 3 lignes ont été insérées
4. Vérification des valeurs insérées
5. Nettoyage des données de test

**Résultat attendu**:
```
✓ Message published to MQTT
✓ Found 3 measurements in database
✓ humidite: 60.0 (correct)
✓ pression: 1015.0 (correct)
✓ temperature: 22.5 (correct)
✓ Test data cleaned up
✅ PASSED: Integration test
```

---

## Validation plages de valeurs

Les tests vérifient les plages définies dans la spécification:

| Mesure | Min | Max | Unité |
|--------|-----|-----|-------|
| Température | -50.0 | 100.0 | °C |
| Humidité | 0.0 | 100.0 | % |
| Pression | 900.0 | 1100.0 | hPa |

## Dépannage

### Erreur: "Configuration incomplete in .env file"
→ Vérifier que toutes les variables sont définies dans `.env`

### Erreur: "Connection refused" (MQTT)
→ Vérifier: `sudo systemctl status mosquitto`
→ Démarrer: `sudo systemctl start mosquitto`

### Erreur: "Access denied" (MySQL)
→ Vérifier les credentials dans `.env`
→ Vérifier les permissions utilisateur dans MySQL

### Erreur: "Table 'mesures' does not exist"
→ Exécuter: `mysql -u dba -p < /path/to/database/creation.sql`

### subscriber.py ne reçoit pas de messages
→ Vérifier que le topic MQTT est le même dans `.env` et dans Mosquitto
→ Vérifier les logs de subscriber.py pour les erreurs de connexion

## Checklist de validation

- [ ] Test 1: Connexion MQTT réussie
- [ ] Test 2: Connexion MySQL réussie
- [ ] Test 3: Validation messages (warnings corrects dans logs)
- [ ] Test 4: Intégration complète réussie
- [ ] `sender.py` génère et envoie 1440 messages sans erreur
- [ ] `subscriber.py` insère correctement les données en base
- [ ] Arrêt propre de `subscriber.py` avec Ctrl+C (logs de fermeture)
- [ ] Visualisation possible dans Grafana/Node-RED

## Notes importantes

1. Les tests 3 et 4 nécessitent que `subscriber.py` soit actif
2. Le test d'intégration insère et nettoie automatiquement les données de test
3. Tous les scripts peuvent être exécutés plusieurs fois sans effet de bord
4. Les tests utilisent la même configuration `.env` que les scripts principaux
