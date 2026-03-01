# Mock Robot Niryo

Simulateur du script `script7_API_mqtt.py` qui tourne sur le robot Niryo.
Permet de tester les séances 3 et 4 du TP sans robot physique.

## Ce que fait le mock

- Expose une API Flask sur le port 3000 (identique au vrai robot)
- Simule le clignotement LED par un délai de 2 secondes
- Publie les événements MQTT sur `robot3/events` après chaque action

## Installation

```bash
cd code/mock_robot
pip install -r requirements.txt
```

## Configuration

Éditer le fichier `.env` pour adapter les paramètres :

```ini
# Flask
API_HOST=0.0.0.0
API_PORT=3000

# MQTT
MQTT_BROKER=192.168.1.3
MQTT_PORT=1883
MQTT_USER=nuc
MQTT_PASSWORD=nuc
MQTT_TOPIC=robot3/events
```

## Lancement

```bash
python3 app.py
```

## Endpoints

### `POST /color`

Simule le clignotement LED dans la couleur demandée.

```bash
curl -X POST http://localhost:3000/color \
     -H "Content-Type: application/json" \
     -d '{"color": "red"}'
```

Couleurs acceptées : `red`, `green`, `blue`.

Réponse succès (200) :
```json
{"status": "ok", "color": "red"}
```

Réponse erreur (400) :
```json
{"error": "Couleur inconnue"}
```

## Messages MQTT publiés

Chaque action publie un événement JSON sur le topic configuré :

```json
{"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
```

```json
{"event": "color_error", "timestamp": 1709136000.0, "data": {"color": "yellow"}}
```

```json
{"event": "calibration_done", "timestamp": 1709136000.0, "data": {"status": "success"}}
```

## Vérification

Observer les messages MQTT publiés par le mock :

```bash
mosquitto_sub -h localhost -p 1883 -t "robot3/events" -u nuc -P nuc
```
