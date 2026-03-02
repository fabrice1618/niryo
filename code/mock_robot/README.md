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
MOCK_API_HOST=0.0.0.0
MOCK_API_PORT=3000

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

Couleurs acceptées : `red`, `green`, `blue`.

Réponse succès (200) :
```json
{"status": "ok", "color": "red"}
```

Réponse erreur (400) :
```json
{"error": "Couleur inconnue"}
```

## Tester l'API

### Avec curl

`curl` est l'outil en ligne de commande standard pour envoyer des requêtes HTTP.

Envoyer une couleur valide :
```bash
curl -X POST http://localhost:3000/color \
     -H "Content-Type: application/json" \
     -d '{"color": "red"}'
```

Tester une couleur invalide :
```bash
curl -X POST http://localhost:3000/color \
     -H "Content-Type: application/json" \
     -d '{"color": "yellow"}'
```

Tester sans body (erreur 400) :
```bash
curl -X POST http://localhost:3000/color \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Avec diag_api (recommandé)

L'outil `diag_api` (dans `code/diag_api/`) est un script interactif dédié au diagnostic de l'API robot. Il affiche la configuration, propose les couleurs disponibles, et formate la réponse. C'est l'outil recommandé pour les TP.

```bash
cd code/diag_api
python3 diag_api.py
```

L'outil lit la configuration depuis le fichier `.env` à la racine du projet (variable `MOCK_API_PORT`).

Voir le [README de diag_api](../diag_api/README.md) pour plus de détails.

## Messages MQTT publiés

Chaque action publie un événement JSON sur le topic configuré :

```json
{"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
```

```json
{"event": "color_error", "timestamp": 1709136000.0, "data": {"color": "yellow"}}
```

## Vérification

Observer les messages MQTT publiés par le mock :

```bash
cd code/diag_mqtt
python3 diag_mqtt.py
```
