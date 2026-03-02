# Diagnostic API — TP Niryo

Outil interactif pour tester l'API du robot Niryo (ou de son mock).
Équivalent de `diag_mqtt` mais pour les requêtes HTTP vers l'API Flask du robot.

## Ce que fait l'outil

- Affiche la configuration API en cours (hôte, port)
- Propose un menu interactif pour choisir la couleur à envoyer
- Envoie la requête `POST /color` et affiche la réponse formatée
- Permet la saisie libre pour tester les cas d'erreur

## Installation

```bash
cd code/diag_api
pip install requests python-dotenv
```

## Utilisation

```bash
python3 diag_api.py
```

Exemple de session :

```
========================================
  Diagnostic API — TP Niryo
========================================
  URL      : http://localhost:3000
========================================

Couleur à envoyer :
  1. red
  2. green
  3. blue
  4. Saisie libre (test erreur)
Choix [1/2/3/4] : 1

Requête POST http://localhost:3000/color
  Body : {"color": "red"}

Réponse HTTP 200 :
  {
    "status": "ok",
    "color": "red"
  }
```

## Configuration

L'outil lit le fichier `.env` à la racine du projet :

```ini
DIAG_API_PORT=3000
DIAG_API_HOST=localhost
```
