# MQTT Message Handler - Spécification technique

## 1. Vue d'ensemble

Ce module contient deux scripts Python pour gérer les messages MQTT de capteurs:
- **subscriber.py**: Reçoit les messages MQTT et les stocke dans MySQL
- **sender.py**: Génère et envoie des données de test sur 24 heures

## 2. Prérequis techniques

- **Python**: Version 3.8 ou supérieure
- **MySQL**: Base de données robot1 configurée (voir `/database/creation.sql`)
- **MQTT Broker**: Mosquitto avec authentification sur port 1883
- **Dépendances Python**: voir `requirements.txt`
  - `paho-mqtt>=1.6.1` - Client MQTT
  - `pymysql>=1.0.2` - Connecteur MySQL
  - `python-dotenv>=1.0.0` - Gestion variables d'environnement

## 3. Configuration (.env)

Créer un fichier `.env` à la racine du module avec les paramètres suivants:

```bash
# MQTT Configuration
MQTT_BROKER=192.168.1.2
MQTT_PORT=1883
MQTT_USER=robot1
MQTT_PASSWORD=xxxxx
MQTT_TOPIC=exemple/capteur

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=robot1
MYSQL_PASSWORD=robot1pass
MYSQL_DATABASE=robot1
```

**Note**: Le fichier `.env` ne doit PAS être commité dans Git. Créer un fichier `.env.example` avec la structure mais sans les vrais mots de passe.

## 4. Script 1: subscriber.py (Récepteur MQTT → MySQL)

### 4.1 Fonctionnalités

1. Chargement de la configuration depuis `.env`
2. Connexion au broker MQTT avec authentification
3. Souscription au topic `exemple/capteur`
4. Connexion à la base de données MySQL `robot1`
5. Réception et validation des messages JSON
6. Insertion des mesures dans la table `mesures`
7. Logging des opérations et erreurs
8. Gestion propre de l'arrêt (SIGINT/SIGTERM)

### 4.2 Format des messages attendus

```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "temperature": 23.5,
  "humidite": 65.2,
  "pression": 1013.25
}
```

**Clés obligatoires**: `timestamp`, `temperature`, `humidite`, `pression`

### 4.3 Règles de validation

#### Validation de structure JSON
- Le payload doit être un JSON valide
- Toutes les clés obligatoires doivent être présentes
- Format timestamp: `YYYY-MM-DD HH:MM:SS` (ex: `2025-12-23 14:35:00`)
- Les valeurs numériques doivent être de type `float` ou `int`

#### Validation des plages de valeurs
- **température**: `-50.0` à `100.0` °C
- **humidite**: `0.0` à `100.0` %
- **pression**: `900.0` à `1100.0` hPa

### 4.4 Insertion dans la base de données

Pour chaque message valide, **3 insertions** sont effectuées dans la table `mesures`:

```sql
INSERT INTO mesures (timestamp, cle, valeur) VALUES ('2025-12-23 14:35:00', 'temperature', 23.5);
INSERT INTO mesures (timestamp, cle, valeur) VALUES ('2025-12-23 14:35:00', 'humidite', 65.2);
INSERT INTO mesures (timestamp, cle, valeur) VALUES ('2025-12-23 14:35:00', 'pression', 1013.25);
```

**Structure de la table** (définie dans `/database/creation.sql`):
```sql
mesures (
    mesure_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    cle VARCHAR(50) NOT NULL,
    valeur FLOAT NOT NULL
)
```

### 4.5 Gestion des erreurs

| Type d'erreur | Comportement |
|--------------|--------------|
| Erreur connexion MQTT | Log ERROR + exit(1) |
| Erreur connexion MySQL | Log ERROR + exit(1) |
| JSON invalide | Log WARNING + ignore message + continue |
| Clé manquante | Log WARNING + ignore message + continue |
| Valeur hors plage | Log WARNING + ignore cette mesure + continue avec les autres |
| Erreur insertion SQL | Log ERROR + continue |

### 4.6 Logging

**Format**: `[TIMESTAMP] [NIVEAU] Message`

**Niveaux**:
- `INFO`: Connexions établies, messages valides traités
- `WARNING`: Validation échouée, données ignorées
- `ERROR`: Erreurs de connexion, erreurs critiques

**Sortie**: Console (stdout pour INFO, stderr pour WARNING/ERROR)

**Exemples**:
```
[2025-12-23 14:35:12] INFO Connexion MQTT établie sur 192.168.1.2:1883
[2025-12-23 14:35:13] INFO Connexion MySQL établie sur robot1
[2025-12-23 14:35:14] INFO Souscription au topic: exemple/capteur
[2025-12-23 14:35:20] INFO Message reçu et traité: 3 mesures insérées
[2025-12-23 14:35:25] WARNING JSON invalide ignoré: Expecting value: line 1 column 1
[2025-12-23 14:35:30] WARNING Valeur hors plage ignorée: temperature=150.5
```

### 4.7 Comportement d'arrêt

- **Durée d'exécution**: Le script tourne jusqu'à interruption manuelle (Ctrl+C)
- **Gestion des signaux**: Capture SIGINT/SIGTERM pour fermeture propre
- **Arrêt propre**:
  1. Fermeture de la connexion MQTT
  2. Fermeture de la connexion MySQL
  3. Log de fin d'exécution
  4. Exit code 0

## 5. Script 2: sender.py (Générateur de données test)

### 5.1 Fonctionnalités

1. Chargement de la configuration depuis `.env`
2. Connexion au broker MQTT avec authentification
3. Génération de 1440 messages (24h à 1 message/minute)
4. Publication sur le topic `exemple/capteur`
5. Données réalistes avec variations cohérentes
6. Arrêt propre en cas d'erreur

### 5.2 Stratégie de génération des données

**Période**: 24 heures (1440 minutes)
**Fréquence**: 1 message par minute
**Total**: 1440 messages

**Point de départ timestamp**: Date/heure actuelle - 24h
**Incrément**: +1 minute par message

### 5.3 Valeurs générées (réalistes et cohérentes)

#### Température (°C)
- **Oscillation quotidienne**: Variation sinusoïdale sur 24h
- **Plage**: 15°C (nuit) à 25°C (après-midi)
- **Variation aléatoire**: ±1°C pour réalisme
- **Formule**: `20 + 5 * sin(2π * heure/24) + random(-1, 1)`

#### Humidité (%)
- **Corrélation inverse** avec température
- **Plage**: 40% (chaud) à 80% (frais)
- **Variation aléatoire**: ±3%
- **Formule**: `60 - 20 * sin(2π * heure/24) + random(-3, 3)`

#### Pression atmosphérique (hPa)
- **Variation lente** (tendance météo)
- **Plage**: 1010 à 1020 hPa
- **Variation aléatoire**: ±0.5 hPa
- **Formule**: `1015 + 5 * sin(2π * heure/48) + random(-0.5, 0.5)`

### 5.4 Format de publication

Chaque message publié respecte le format JSON attendu par le subscriber:

```json
{
  "timestamp": "2025-12-23 14:35:00",
  "temperature": 21.5,
  "humidite": 62.3,
  "pression": 1013.2
}
```

### 5.5 Stratégie d'envoi

**Option retenue**: Génération et envoi immédiat en boucle rapide

- Génération de chaque message
- Publication immédiate sur MQTT
- Pas de pause entre messages
- Durée totale d'exécution: quelques secondes

**Justification**: Pour un TP pédagogique, le remplissage rapide de la base de données permet de tester rapidement les visualisations Grafana/Node-RED.

**Alternative possible** (non retenue): Ajouter `time.sleep(0.1)` entre messages pour simuler temps réel accéléré (144x).

### 5.6 Gestion des erreurs

| Type d'erreur | Comportement |
|--------------|--------------|
| Erreur connexion MQTT | Log ERROR + exit(1) |
| Erreur publication MQTT | Log ERROR + exit(1) |

### 5.7 Logging

**Format**: `[TIMESTAMP] [NIVEAU] Message`

**Exemples**:
```
[2025-12-23 14:35:12] INFO Connexion MQTT établie sur 192.168.1.2:1883
[2025-12-23 14:35:13] INFO Génération de 1440 messages sur 24 heures
[2025-12-23 14:35:13] INFO Publication du message 1/1440
[2025-12-23 14:35:14] INFO Publication du message 100/1440
...
[2025-12-23 14:35:20] INFO Tous les messages ont été publiés avec succès
[2025-12-23 14:35:20] INFO Fermeture de la connexion MQTT
```

## 6. Structure des fichiers

```
code/mqtt_message/
├── .env                    # Configuration (CRÉER, ne pas commiter)
├── .env.example            # Exemple de configuration (à créer)
├── requirements.txt        # Dépendances Python
├── specification.md        # Ce fichier
├── subscriber.py           # Script récepteur MQTT → MySQL (à créer)
└── sender.py               # Script générateur de données (à créer)
```

## 7. Utilisation

### 7.1 Installation

```bash
cd code/mqtt_message
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec les vrais paramètres
```

### 7.2 Exécution

**Générer des données test**:
```bash
python sender.py
```

**Recevoir et stocker les données**:
```bash
python subscriber.py
# Ctrl+C pour arrêter proprement
```

**Dans un scénario typique**:
1. Terminal 1: Lancer `subscriber.py` (écoute continue)
2. Terminal 2: Lancer `sender.py` (génère 1440 messages)
3. Terminal 1: Observer les logs de réception
4. Vérifier dans Grafana que les données sont présentes

## 8. Checklist de validation pré-implémentation

**À valider avant d'écrire le code:**

- [ ] Structure du fichier `.env` confirmée
- [ ] Noms des scripts: `subscriber.py` et `sender.py`
- [ ] Plages de validation des valeurs confirmées:
  - [ ] Température: -50 à 100°C
  - [ ] Humidité: 0 à 100%
  - [ ] Pression: 900 à 1100 hPa
- [ ] Stratégie d'envoi du sender: envoi immédiat en boucle rapide (pas de pause)
- [ ] Format de logging: `[TIMESTAMP] [NIVEAU] Message`
- [ ] Comportement en cas d'erreur:
  - [ ] Erreurs connexion → exit(1)
  - [ ] Validation échouée → warning + continue
- [ ] Structure de la table `mesures` vérifiée (conforme à `database/creation.sql`)
- [ ] Format du timestamp compatible MySQL: `YYYY-MM-DD HH:MM:SS`
- [ ] Insertion de 3 lignes par message confirmée (une par clé)
- [ ] Gestion propre de SIGINT/SIGTERM pour arrêt du subscriber

## 9. **Ne pas executer** de Tests à effectuer après implémentation. Nous ne sommes pas sur la plateforme cible

1. **Test connexion MQTT**: Vérifier connexion au broker avec authentification
2. **Test connexion MySQL**: Vérifier connexion à la base robot1
3. **Test sender**: Générer 1440 messages et vérifier publication
4. **Test subscriber**: Recevoir et stocker des messages
5. **Test validation JSON**: Envoyer JSON invalide et vérifier warning
6. **Test validation plages**: Envoyer valeurs hors plage et vérifier warning
7. **Test base données**: Vérifier que 3 lignes sont insérées par message
8. **Test arrêt propre**: Ctrl+C sur subscriber et vérifier fermeture propre
9. **Test visualisation**: Vérifier dans Grafana que les données sont exploitables
