# Site web de pilotage — TP Niryo

Interface web pour envoyer des commandes couleur au robot Niryo (mock ou réel) via l'API Flask.

## Installation

Les dépendances sont déjà incluses dans le `venv` du projet. Sinon :

```bash
pip install -r requirements.txt
```

## Lancement

### Depuis la racine du projet (recommandé)

```bash
./website_pilotage.sh
```

### Avec override de l'IP du robot réel

```bash
python code/website_pilotage/app.py --robot-ip 192.168.1.13
```

## Configuration

Les cibles sont lues depuis le fichier `.env` racine :

| Variable         | Rôle                        | Défaut          |
|------------------|-----------------------------|-----------------|
| `MOCK_API_HOST`  | IP du mock robot            | `localhost`     |
| `MOCK_API_PORT`  | Port du mock robot          | `3000`          |
| `ROBOT_API`      | IP du robot réel            | `192.168.1.13`  |
| `ROBOT_PORT`     | Port du robot réel          | `3000`          |

L'argument `--robot-ip` permet de surcharger `ROBOT_API` sans modifier le `.env`.

## Utilisation

1. Lancer le mock robot (ou le robot réel) : `./run_mock.sh`
2. Lancer le site : `./website_pilotage.sh`
3. Ouvrir http://localhost:5000 dans un navigateur
4. **Sélectionner la cible** (mock ou robot) via le menu déroulant
5. Cliquer sur les boutons Rouge / Vert / Bleu
6. Utiliser la **saisie libre** pour tester une couleur invalide (ex : `yellow`) et observer l'erreur
7. Observer la réponse JSON de l'API

## Architecture

```
Navigateur  ──GET /──►  Flask (port 5000)  ──page HTML──►  Navigateur
Navigateur  ──POST /send_color──►  Flask  ──POST /color──►  Robot API (port 3000)
```

Le serveur Flask sert de **proxy** : il relaie les commandes du navigateur vers l'API du robot sélectionné. Cela évite les problèmes CORS (le navigateur ne contacte qu'un seul serveur).
