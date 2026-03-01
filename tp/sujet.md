# Robot Niryo dans un environnement client/serveur

Mettre en oeuvre une architecture distribuée permettant :

- le pilotage d'un robot Niryo Ned2
- le pilotage du robot via une API Flask
- la transmission d'informations via MQTT
- le traitement des messages en Python
- le stockage en base SQL
- la supervision via Grafana

---

## Organisation pédagogique

### Durée conseillée

6 séances de 3h30

### Compétences visées

- Architecture client/serveur
- Communication MQTT
- API REST
- Base de données SQL
- Supervision industrielle
- Robotique collaborative

---

## Progression pédagogique

---

## Séance 1 — Prise en main du robot Niryo Ned2

### Objectifs

- Comprendre le fonctionnement du robot
- Tester les scripts fournis
- Découvrir l'API Python du Niryo

### Activités

1. Connexion au robot
2. Exécution d'un script simple :
   - Homing
   - Déplacement en coordonnées cartésiennes
   - Ouverture/fermeture pince
3. Création d'un petit scénario :
   - Pick & Place simple

### Compétences validées

- Connexion robot
- Lancement de scripts
- Compréhension des axes et coordonnées

---

## Séance 2 — Communication MQTT avec le Robot Niryo

### Objectifs

- Comprendre le principe publish/subscribe de MQTT
- Configurer un broker Mosquitto avec authentification
- Faire publier des messages par le robot (publisher)
- Faire réagir le robot à des messages reçus (subscriber)
- Diagnostiquer les échanges MQTT depuis le serveur

### Rappel théorique

MQTT fonctionne sur un modèle **publish/subscribe** :

```
Publisher  ──publish──►  Broker  ──deliver──►  Subscriber
              (topic)   (Mosquitto)              (topic)
```

- **Topic** : canal de communication (ex : `hello`)
- **Broker** : serveur central qui route les messages (Mosquitto, port 1883)
- **QoS** : niveau de garantie de livraison (0 = au mieux, 1 = au moins une fois, 2 = exactement une fois)

Paramètres de connexion :
```
Broker IP   : 192.168.1.3
Port        : 1883
Identifiant : mqtt
Mot de passe : mqtt
Topic       : hello
```

---

### Partie 1 — Le robot publie des messages MQTT

#### Objectif

Le robot Niryo envoie un message MQTT toutes les secondes sur le topic `hello`. On observe les messages depuis le serveur.

#### Script : `script4_mqtt_send.py`

Analyse du script :

```python
# Connexion MQTT avec authentification
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()

# Boucle d'envoi : un message par seconde
while not rospy.is_shutdown():
    client.publish(TOPIC, "hello world")
    time.sleep(1)
```

Le script :
1. Initialise le robot (calibration automatique)
2. Signale le début (LED + son) et la fin de la calibration
3. Se connecte au broker MQTT avec identifiant/mot de passe
4. Publie `"hello world"` sur le topic `hello` chaque seconde

#### Activités

1. **Lire et comprendre** le script `script4_mqtt_send.py`
2. **Lancer le script** sur le robot
3. **Diagnostiquer depuis le serveur** — Ouvrir un terminal sur le serveur et s'abonner au topic pour vérifier la réception :
   ```bash
   mosquitto_sub -h localhost -p 1883 -t "hello" -u mqtt -P mqtt
   ```
   Vous devez voir apparaître `hello world` toutes les secondes.
4. **Modifier le message** : changer `"hello world"` par un message personnalisé, relancer et vérifier côté serveur
5. **Modifier le topic** : utiliser un topic différent (ex : `robot1/status`), adapter la commande `mosquitto_sub` en conséquence

#### Questions

- Que se passe-t-il si le broker n'est pas démarré ?
- Que se passe-t-il si le mot de passe est incorrect ?
- Le message est-il conservé si aucun subscriber n'écoute ?

---

### Partie 2 — Le robot reçoit des messages MQTT

#### Objectif

Le robot Niryo écoute le topic `hello` et réagit aux messages reçus en faisant clignoter son anneau LED dans la couleur demandée.

#### Script : `script5_mqtt_receive.py`

Analyse du script :

```python
# Callback à la connexion : souscription au topic
def on_connect(client, userdata, flags, rc):
    print("MQTT connecté avec code :", rc)
    client.subscribe(TOPIC)

# Callback à la réception d'un message
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("Message reçu :", message)
    blink_color(message)
```

La fonction `blink_color()` fait clignoter le LED ring pendant ~2 secondes dans la couleur demandée (`red`, `green` ou `blue`).

Le script :
1. Initialise le robot (calibration automatique)
2. Se connecte au broker et s'abonne au topic `hello`
3. Attend les messages en boucle
4. À chaque message reçu, fait clignoter les LEDs dans la couleur correspondante

#### Activités

1. **Lire et comprendre** le script `script5_mqtt_receive.py`
2. **Lancer le script** sur le robot
3. **Envoyer un message depuis le serveur** — Ouvrir un terminal et publier une couleur :
   ```bash
   mosquitto_pub -h localhost -p 1883 -t "hello" -u mqtt -P mqtt -m "red"
   ```
4. **Tester les trois couleurs** : envoyer `red`, `green`, `blue` et observer la réaction du robot
5. **Tester une couleur inconnue** : envoyer `yellow` et observer le message d'erreur dans la console du robot
6. **Diagnostiquer depuis le serveur** — Dans un second terminal, observer les messages échangés :
   ```bash
   mosquitto_sub -h localhost -p 1883 -t "hello" -u mqtt -P mqtt -v
   ```

#### Questions

- Quel est le rôle de `on_connect` et `on_message` ?
- Pourquoi la souscription est-elle faite dans `on_connect` plutôt que dans le code principal ?
- Que se passe-t-il si on envoie un message avant que le robot ne soit connecté au broker ?

### Compétences validées

- Comprendre le modèle publish/subscribe
- Configurer un client MQTT avec authentification
- Publier et recevoir des messages MQTT
- Diagnostiquer les échanges MQTT avec `mosquitto_pub` et `mosquitto_sub`
- Comprendre les callbacks MQTT (`on_connect`, `on_message`)

---

## Séance 3 — API Flask de pilotage du Robot

### Objectifs

- Comprendre le rôle d'une API REST
- Lancer une API Flask directement sur le robot
- Envoyer des commandes HTTP au robot depuis le serveur
- Observer la chaîne complète : HTTP → Flask → Robot → MQTT

### Rappel théorique

Une **API REST** permet de piloter un système via des requêtes HTTP standard (GET, POST, PUT, DELETE). Flask est un micro-framework Python qui permet de créer rapidement une API.

Architecture mise en place :

```
                          ┌──────────────────────────────┐
  Serveur (curl/Postman)  │         Robot Niryo          │
  ───── POST /color ─────►│  Flask (port 3000)           │
                          │   ├── blink_color()          │
                          │   └── publish_mqtt() ────────┼──► Broker MQTT
                          └──────────────────────────────┘     (serveur)
```

Le script `script7_API_mqtt.py` combine :
- Un **serveur Flask** qui écoute les requêtes HTTP sur le port 3000
- Un **client MQTT** qui publie un événement après chaque action
- Le **contrôle du robot** (clignotement LED)

### Script : `script7_API_mqtt.py`

#### Analyse du code

**1. Connexion MQTT :**
```python
BROKER_IP = "192.168.1.3"
BROKER_PORT = 1883
TOPIC = "robot3/events"

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER_IP, BROKER_PORT, 60)
client.loop_start()
```

**2. Fonction de publication MQTT :**
```python
def publish_mqtt(event_type, data):
    payload = {
        "event": event_type,
        "timestamp": time.time(),
        "data": data
    }
    client.publish(TOPIC, json.dumps(payload))
```

Chaque événement publié contient : le type d'événement, un timestamp et les données associées.

**3. Endpoint Flask :**
```python
@app.route('/color', methods=['POST'])
def api_color():
    data = request.json
    color = data["color"].lower()

    ok = blink_color(color)

    if not ok:
        publish_mqtt("color_error", {"color": color})
        return jsonify({"error": "Couleur inconnue"}), 400

    publish_mqtt("color_done", {"color": color, "status": "success"})
    return jsonify({"status": "ok", "color": color})
```

L'endpoint `/color` :
- Reçoit une requête POST avec un JSON `{"color": "red"}`
- Fait clignoter les LEDs du robot dans la couleur demandée
- Publie un message MQTT `color_done` (succès) ou `color_error` (échec)
- Retourne une réponse JSON au client

**4. Lancement Flask dans un thread séparé :**
```python
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
```

Flask tourne dans un thread pour ne pas bloquer la boucle ROS principale.

### Activités

#### Partie 1 — Lancement et test de l'API

1. **Lire et comprendre** le script `script7_API_mqtt.py`
2. **Adapter les paramètres** : vérifier l'IP du broker et le topic MQTT selon votre configuration
3. **Lancer le script** sur le robot
4. **Tester l'API depuis le serveur** avec `curl` :
   ```bash
   # Envoyer la couleur rouge
   curl -X POST http://<IP_ROBOT>:3000/color \
        -H "Content-Type: application/json" \
        -d '{"color": "red"}'
   ```
5. **Tester les trois couleurs** :
   ```bash
   curl -X POST http://<IP_ROBOT>:3000/color -H "Content-Type: application/json" -d '{"color": "green"}'
   curl -X POST http://<IP_ROBOT>:3000/color -H "Content-Type: application/json" -d '{"color": "blue"}'
   ```
6. **Tester une erreur** — envoyer une couleur inconnue :
   ```bash
   curl -X POST http://<IP_ROBOT>:3000/color -H "Content-Type: application/json" -d '{"color": "yellow"}'
   ```
   Observer le code de retour HTTP 400 et le message d'erreur JSON.

#### Partie 2 — Diagnostics MQTT côté serveur

1. **Observer les événements MQTT** — Sur le serveur, s'abonner au topic du robot :
   ```bash
   mosquitto_sub -h localhost -p 1883 -t "robot3/events" -u nuc -P nuc
   ```
2. **Envoyer des commandes** depuis un autre terminal et observer les messages MQTT reçus :
   - Un message `color_done` doit apparaître pour chaque couleur valide
   - Un message `color_error` doit apparaître pour une couleur inconnue
3. **Analyser le format JSON** des messages reçus :
   ```json
   {"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
   ```
4. **Vérifier la connectivité** — En cas de problème :
   ```bash
   # Vérifier que le broker est actif
   systemctl status mosquitto

   # Vérifier que le port 3000 du robot est accessible
   curl -s -o /dev/null -w "%{http_code}" http://<IP_ROBOT>:3000/color

   # Lister les clients connectés au broker
   mosquitto_sub -h localhost -p 1883 -t '$SYS/broker/clients/connected' -u nuc -P nuc
   ```

#### Questions

- Pourquoi Flask est-il lancé dans un thread séparé ?
- Quel est l'intérêt de publier un message MQTT après chaque action alors que l'API retourne déjà une réponse ?
- Que se passe-t-il si deux requêtes HTTP arrivent en même temps ?
- Quelle est la différence entre les codes HTTP 200 et 400 retournés par l'API ?

### Compétences validées

- Comprendre une API REST (endpoint, méthode POST, JSON)
- Tester une API avec `curl`
- Observer la chaîne complète HTTP → Flask → Robot → MQTT
- Diagnostiquer avec `mosquitto_sub` et `curl`
- Comprendre le threading Python pour Flask

---

## Séance 4 — Handler Python + Base SQL

### Objectifs

- Créer la table `events` en base de données MySQL
- Comprendre le handler Python qui reçoit les messages MQTT et les stocke en base
- Connecter la chaîne complète : Robot → MQTT → Handler → MySQL
- Vérifier les données enregistrées avec des requêtes SQL

### Rappel théorique

En séance 3, le robot publie des événements MQTT au format JSON sur le topic `robot3/events` :

```json
{"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
{"event": "color_error", "timestamp": 1709136000.0, "data": {"color": "yellow"}}
```

Le **handler** est un script Python qui tourne sur le serveur. Il :
1. S'abonne au topic MQTT `robot3/events`
2. Décode le message JSON
3. Convertit le timestamp epoch en datetime
4. Insère l'événement dans la table MySQL `events`

```
Robot (Flask+MQTT)  ──publish──►  Broker  ──deliver──►  Handler  ──INSERT──►  MySQL
   (séance 3)                   Mosquitto              event_handler.py       (events)
```

---

### Partie 1 — Création de la table `events`

#### Script SQL : `database/creation_events.sql`

```sql
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL COMMENT 'Horodatage (converti depuis epoch)',
    event_type VARCHAR(50) NOT NULL COMMENT 'Type : color_done, color_error',
    color VARCHAR(20) DEFAULT NULL COMMENT 'Couleur demandée',
    status VARCHAR(20) DEFAULT NULL COMMENT 'Résultat : success, error',
    raw_json TEXT NOT NULL COMMENT 'Message JSON brut reçu via MQTT',
    INDEX idx_timestamp (timestamp),
    INDEX idx_event_type (event_type),
    INDEX idx_timestamp_event (timestamp, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### Activités

1. **Créer la table** sur le serveur :
   ```bash
   mysql -u robot3 -probot3pass robot3 < database/creation_events.sql
   ```
2. **Vérifier la structure** :
   ```bash
   mysql -u robot3 -probot3pass robot3 -e "DESCRIBE events;"
   ```
   Résultat attendu :
   ```
   +------------+--------------+------+-----+---------+----------------+
   | Field      | Type         | Null | Key | Default | Extra          |
   +------------+--------------+------+-----+---------+----------------+
   | event_id   | int          | NO   | PRI | NULL    | auto_increment |
   | timestamp  | datetime     | NO   | MUL | NULL    |                |
   | event_type | varchar(50)  | NO   | MUL | NULL    |                |
   | color      | varchar(20)  | YES  |     | NULL    |                |
   | status     | varchar(20)  | YES  |     | NULL    |                |
   | raw_json   | text         | NO   |     | NULL    |                |
   +------------+--------------+------+-----+---------+----------------+
   ```

#### Questions

- Pourquoi garder le champ `raw_json` alors que les données sont déjà décomposées ?
- Quel est le rôle des index `idx_timestamp` et `idx_event_type` ?
- Pourquoi `color` et `status` sont `NULL`-ables ?

---

### Partie 2 — Handler Python `event_handler.py`

#### Configuration

Le handler utilise un fichier `.env` pour ses paramètres. Copier le modèle et l'adapter :

```bash
cd code/mqtt_message
cp .env.events.example .env
```

Contenu du fichier `.env` :
```ini
# MQTT
MQTT_BROKER=192.168.1.3
MQTT_PORT=1883
MQTT_USER=nuc
MQTT_PASSWORD=nuc
MQTT_TOPIC=robot3/events

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=robot3
MYSQL_PASSWORD=robot3pass
MYSQL_DATABASE=robot3
```

#### Analyse du script `event_handler.py`

**1. Callback de réception MQTT — décodage et extraction :**
```python
def on_message(client, userdata, msg):
    raw = msg.payload.decode()
    data = json.loads(raw)

    event_type = data.get("event")          # "color_done" ou "color_error"
    ts_epoch = data.get("timestamp")        # 1709136000.0
    event_data = data.get("data", {})       # {"color": "red", "status": "success"}

    # Conversion timestamp epoch → datetime
    ts = datetime.fromtimestamp(float(ts_epoch))

    color = event_data.get("color")
    status = event_data.get("status")
```

**2. Insertion en base de données :**
```python
    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT INTO events (timestamp, event_type, color, status, raw_json) "
        "VALUES (%s, %s, %s, %s, %s)",
        (ts, event_type, color, status, raw)
    )
    db_conn.commit()
```

Le handler utilise des **requêtes paramétrées** (`%s`) pour se protéger des injections SQL.

#### Activités

1. **Lire et comprendre** le script `code/mqtt_message/event_handler.py`
2. **Installer les dépendances** (si pas déjà fait) :
   ```bash
   cd code/mqtt_message
   pip install paho-mqtt pymysql python-dotenv
   ```
3. **Lancer le handler** sur le serveur :
   ```bash
   python3 event_handler.py
   ```
   Sortie attendue :
   ```
   [2026-02-28 10:00:00] INFO Connexion MySQL établie (robot3)
   [2026-02-28 10:00:00] INFO Connecté au broker MQTT
   [2026-02-28 10:00:00] INFO Souscription au topic: robot3/events
   [2026-02-28 10:00:00] INFO En attente d'événements MQTT (Ctrl+C pour arrêter)...
   ```

#### Questions

- Que fait `datetime.fromtimestamp()` ? Pourquoi ne pas stocker directement le timestamp epoch ?
- Pourquoi utiliser `%s` plutôt que des f-strings pour la requête SQL ?
- Que se passe-t-il si la base MySQL n'est pas accessible au démarrage ?

---

### Partie 3 — Test de la chaîne complète

#### Activités

1. **Sur le serveur** — Lancer le handler dans un premier terminal :
   ```bash
   cd code/mqtt_message
   python3 event_handler.py
   ```

2. **Sur le robot** — Lancer l'API Flask (séance 3) :
   ```bash
   python3 script7_API_mqtt.py
   ```

3. **Depuis le serveur** — Envoyer des commandes dans un second terminal :
   ```bash
   # Commande réussie
   curl -X POST http://<IP_ROBOT>:3000/color \
        -H "Content-Type: application/json" \
        -d '{"color": "red"}'

   # Commande en erreur
   curl -X POST http://<IP_ROBOT>:3000/color \
        -H "Content-Type: application/json" \
        -d '{"color": "yellow"}'
   ```

4. **Observer les logs du handler** — Vous devez voir :
   ```
   [2026-02-28 10:01:00] INFO Message reçu: {"event": "color_done", ...}
   [2026-02-28 10:01:00] INFO Événement inséré: color_done color=red status=success
   [2026-02-28 10:01:15] INFO Message reçu: {"event": "color_error", ...}
   [2026-02-28 10:01:15] INFO Événement inséré: color_error color=yellow status=None
   ```

5. **Vérifier en base de données** :
   ```bash
   # Afficher tous les événements
   mysql -u robot3 -probot3pass robot3 -e "SELECT * FROM events ORDER BY timestamp DESC;"

   # Compter les événements par type
   mysql -u robot3 -probot3pass robot3 -e "SELECT event_type, COUNT(*) AS nb FROM events GROUP BY event_type;"

   # Afficher les erreurs uniquement
   mysql -u robot3 -probot3pass robot3 -e "SELECT timestamp, color FROM events WHERE event_type = 'color_error';"

   # Afficher les événements des 10 dernières minutes
   mysql -u robot3 -probot3pass robot3 -e "SELECT * FROM events WHERE timestamp > NOW() - INTERVAL 10 MINUTE;"
   ```

6. **Test sans le robot** — On peut aussi tester le handler seul en publiant un message MQTT manuellement :
   ```bash
   mosquitto_pub -h localhost -p 1883 -t "robot3/events" -u nuc -P nuc \
     -m '{"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "green", "status": "success"}}'
   ```

---

### Partie 4 — Diagnostics serveur

1. **Vérifier que le broker MQTT est actif** :
   ```bash
   systemctl status mosquitto
   ```
2. **Vérifier que MySQL est actif** :
   ```bash
   systemctl status mysql
   ```
3. **Tester la connexion MySQL** :
   ```bash
   mysql -u robot3 -probot3pass robot3 -e "SELECT 1;"
   ```
4. **Observer les messages MQTT en temps réel** (dans un terminal séparé) :
   ```bash
   mosquitto_sub -h localhost -p 1883 -t "robot3/events" -u nuc -P nuc -v
   ```
5. **Vérifier le nombre d'enregistrements** :
   ```bash
   mysql -u robot3 -probot3pass robot3 -e "SELECT COUNT(*) AS total FROM events;"
   ```

### Compétences validées

- Créer une table SQL adaptée au format des données
- Comprendre un handler MQTT → SQL (subscriber, décodage JSON, insertion)
- Requêtes SQL : INSERT, SELECT, COUNT, GROUP BY, WHERE
- Diagnostiquer la chaîne complète Robot → MQTT → Handler → MySQL
- Traçabilité industrielle des actions robot

---


## Séance 5 — Supervision avec Grafana

### Objectifs

- Visualiser les données SQL
- Créer un dashboard de suivi robot

### Activités

1. Connexion Grafana à la base SQL
2. Création de graphiques :
   - Nombre de mouvements
   - Répartition des positions
   - Temps d'exécution
3. Ajout d'un indicateur d'état

### Compétences validées

- Supervision industrielle
- Lecture de données temps réel
- Indicateurs de performance

---

## Séance 6 — TP Final : Scénario industriel complet

### Mise en situation

Vous devez mettre en place une cellule robotisée pilotable à distance permettant :

- la prise d'un objet
- la dépose en zone définie
- l'enregistrement des mouvements
- la supervision temps réel

### Travail demandé

1. Créer un scénario de pick & place automatisé
2. Le piloter via :
   - MQTT direct
   - API HTTP
3. Vérifier l'enregistrement en base
4. Créer un dashboard de suivi
5. Analyser :
   - latence
   - fiabilité
   - traçabilité

---

## Vue globale de la progression

| Séance | Niveau | Technologie | Complexité |
|--------|--------|-------------|------------|
| 1 | Robot seul | Niryo | Faible |
| 2 | Communication | MQTT | Moyenne |
| 3 | Middleware | Python + SQL | Moyenne |
| 4 | API | Flask | Élevée |
| 5 | Supervision | Grafana | Élevée |
| 6 | Intégration | Full stack | Très élevée |

---

## Option avancée

- Ajout gestion d'erreurs
- QoS MQTT
- Sécurisation (authentification broker, chiffrement TLS)
- Gestion multi-robots
- Analyse statistique des données
