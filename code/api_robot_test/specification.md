# API Robot Test - Spécification

## Vue d'ensemble

API Flask mock simulant le comportement de l'API de contrôle du robot Niryo. Permet de tester les interfaces web et les clients API sans connexion physique au robot.

## Objectif pédagogique

Permettre aux étudiants de :
- Développer et tester leurs applications de contrôle sans monopoliser le robot
- Comprendre le fonctionnement d'une API REST
- Simuler des scénarios d'erreur (robot non calibré, erreurs de connexion)
- Valider leurs interfaces web avant déploiement sur le système réel

## Endpoints

### POST /autocalibrate

Simule la calibration automatique du robot.

**Requête**
```http
POST /autocalibrate HTTP/1.1
Content-Type: application/json
```

**Corps (optionnel)**
```json
{
  "timeout": 30
}
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Calibration automatique terminée",
  "duration": 2.5
}
```

**Réponse erreur (500)**
```json
{
  "status": "error",
  "message": "Échec de la calibration",
  "error_code": "CALIBRATION_FAILED"
}
```

### POST /color/red

Simule la séquence de manipulation d'un objet rouge.

**Requête**
```http
POST /color/red HTTP/1.1
Content-Type: application/json
```

**Corps (optionnel)**
```json
{
  "speed": 50,
  "precision": "high"
}
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence rouge exécutée",
  "color": "red",
  "execution_time": 3.2,
  "position": {
    "x": 0.2,
    "y": 0.15,
    "z": 0.1
  }
}
```

**Réponse erreur - Robot non calibré (400)**
```json
{
  "status": "error",
  "message": "Robot non calibré. Exécutez /autocalibrate d'abord",
  "error_code": "NOT_CALIBRATED"
}
```

### POST /color/blue

Simule la séquence de manipulation d'un objet bleu.

**Requête**
```http
POST /color/blue HTTP/1.1
Content-Type: application/json
```

**Corps (optionnel)**
```json
{
  "speed": 50,
  "precision": "high"
}
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence bleue exécutée",
  "color": "blue",
  "execution_time": 3.5,
  "position": {
    "x": 0.2,
    "y": -0.15,
    "z": 0.1
  }
}
```

### POST /color/green

Simule la séquence de manipulation d'un objet vert.

**Requête**
```http
POST /color/green HTTP/1.1
Content-Type: application/json
```

**Corps (optionnel)**
```json
{
  "speed": 50,
  "precision": "high"
}
```

**Réponse succès (200)**
```json
{
  "status": "success",
  "message": "Séquence verte exécutée",
  "color": "green",
  "execution_time": 3.1,
  "position": {
    "x": 0.0,
    "y": 0.2,
    "z": 0.1
  }
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
  "calibrated": true,
  "connected": true,
  "position": {
    "x": 0.0,
    "y": 0.0,
    "z": 0.2
  },
  "last_operation": "color/red",
  "timestamp": "2025-12-23 10:30:45"
}
```

### POST /reset

Réinitialise l'état du robot simulé (remet calibrated à false).

**Requête**
```http
POST /reset HTTP/1.1
```

**Réponse (200)**
```json
{
  "status": "success",
  "message": "Robot réinitialisé"
}
```

## Comportement

### État de calibration

- Au démarrage, `calibrated = false`
- Toute opération `/color/*` échoue si `calibrated = false`
- `/autocalibrate` met `calibrated = true`
- `/reset` remet `calibrated = false`

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

### Variables d'environnement

```bash
FLASK_HOST=0.0.0.0          # Interface d'écoute
FLASK_PORT=5000             # Port de l'API
FLASK_DEBUG=True            # Mode debug
SIMULATE_ERRORS=False       # Simuler des erreurs aléatoires (10%)
```

### Fichier de configuration

`config.json` (optionnel)
```json
{
  "calibration_duration": 2.5,
  "operation_duration": 3.0,
  "error_rate": 0.0,
  "positions": {
    "red": {"x": 0.2, "y": 0.15, "z": 0.1},
    "blue": {"x": 0.2, "y": -0.15, "z": 0.1},
    "green": {"x": 0.0, "y": 0.2, "z": 0.1}
  }
}
```

## Scénarios de test

### Test 1 : Flux nominal
1. POST `/autocalibrate` → 200 OK
2. POST `/color/red` → 200 OK
3. POST `/color/blue` → 200 OK
4. POST `/color/green` → 200 OK
5. GET `/status` → calibrated=true

### Test 2 : Robot non calibré
1. POST `/color/red` → 400 NOT_CALIBRATED
2. POST `/autocalibrate` → 200 OK
3. POST `/color/red` → 200 OK

### Test 3 : Réinitialisation
1. POST `/autocalibrate` → 200 OK
2. POST `/reset` → 200 OK
3. GET `/status` → calibrated=false
4. POST `/color/blue` → 400 NOT_CALIBRATED

### Test 4 : Simulation d'erreurs
1. Activer `SIMULATE_ERRORS=True`
2. Exécuter séquences multiples
3. Vérifier gestion des erreurs 500

## Utilisation

### Démarrage

```bash
cd code/api_robot_test
python app.py
```

### Test avec curl

```bash
# Calibration
curl -X POST http://localhost:5000/autocalibrate

# Séquence rouge
curl -X POST http://localhost:5000/color/red

# Vérification état
curl http://localhost:5000/status
```

### Test avec Python

```python
import requests

base_url = "http://localhost:5000"

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
| Détection d'objets | Simulée | Caméra/capteurs |
| Connexion TCP robot | Non | Oui (SDK Niryo) |
| Gestion LED | Non | Oui |
| Paramètres avancés | Limités | Complets (PoseObject, vitesse, TCP) |

## Évolutions possibles

- [ ] Ajout endpoint `/pick/{color}` et `/place/{position}`
- [ ] Simulation de la détection d'objets via caméra
- [ ] Interface web de monitoring intégrée
- [ ] Logs persistants en base de données
- [ ] Webhooks pour notifier les événements
- [ ] Mode replay (rejouer une séquence enregistrée)