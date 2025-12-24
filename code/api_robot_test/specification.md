# API Robot Test - Spécification

## Vue d'ensemble

API Flask mock simulant le comportement de l'API de contrôle du robot Niryo. Permet de tester les interfaces web et les clients API sans connexion physique au robot.

## Objectif pédagogique

Permettre aux étudiants de :
- Développer et tester leurs applications de contrôle sans monopoliser le robot
- Comprendre le fonctionnement d'une API REST
- Valider leurs interfaces web avant déploiement sur le système réel

## Endpoints

### POST /autocalibrate

Simule la calibration automatique du robot.

**Requête**
```http
POST /autocalibrate HTTP/1.1
Content-Type: application/json
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Calibration automatique terminée",
  "duration": 2.5
}
```


### POST /color/red

Simule le clignotement du LED ring en rouge.

**Requête**
```http
POST /color/red HTTP/1.1
Content-Type: application/json
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence rouge exécutée",
  "color": "red",
}
```

### POST /color/blue

Simule le clignotement du LED ring en bleu.

**Requête**
```http
POST /color/blue HTTP/1.1
Content-Type: application/json
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence bleue exécutée",
  "color": "blue",
}
```

### POST /color/green

Simule le clignotement du LED ring en vert.

**Requête**
```http
POST /color/green HTTP/1.1
Content-Type: application/json
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence verte exécutée",
  "color": "green",
}
```

### GET /status

Retourne l'état actuel du robot simulé.

**Requête**
```http
GET /status HTTP/1.1
```

**Réponse (200)**
```json
{
  "timestamp": "2025-12-23 10:30:45"
}
```

## Comportement

### Temps de réponse

L'API simule des délais réalistes :
- Calibration : 2-3 secondes
- Séquence couleur : 3-4 secondes
- Status/Reset : < 100ms

### Logs

L'API log chaque requête avec :
- Timestamp
- Endpoint
- Paramètres
- Résultat (succès/erreur)

## Configuration

### Variables d'environnement dans fichier .env

```bash
API_TEST_HOST=0.0.0.0          # Interface d'écoute
API_TEST_PORT=3000             # Port de l'API
API_TEST_DEBUG=True            # Mode debug
```

## Scénarios de test

### Test 1 : Flux nominal
1. POST `/autocalibrate` → 200 OK
2. POST `/color/red` → 200 OK
3. POST `/color/blue` → 200 OK
4. POST `/color/green` → 200 OK
5. GET `/status` → 200 OK

## Utilisation

### Démarrage

```bash
cd code/api_robot_test
python app.py
```

### Test avec curl

```bash
# Calibration
curl -X POST http://localhost:3000/autocalibrate

# Séquence rouge
curl -X POST http://localhost:3000/color/red

# Vérification état
curl http://localhost:3000/status
```

### Test avec Python

```python
import requests

base_url = "http://localhost:3000"

# Calibrer
response = requests.post(f"{base_url}/autocalibrate")
print(response.json())

# Exécuter séquence
response = requests.post(f"{base_url}/color/red")
print(response.json())
```

## Différences avec l'API réelle

| Fonctionnalité | API Test | API Robot Réelle |
|----------------|----------|------------------|
| Délai d'exécution | Simulé (2-4s) | Réel (variable) |
| Mouvements physiques | Non | Oui |
| Gestion LED | Non | Oui |

