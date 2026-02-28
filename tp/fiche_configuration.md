# FICHE DE CONFIGURATION INDIVIDUELLE
## TP Robot Niryo Ned2 — Architecture MQTT / API / SQL / Grafana


## 1. Robot Niryo Ned2

| Paramètre | Valeur |
|------------|--------|
| IP Robot | `192.168.1.1X` |
| Nom robot | `ned2_XX` |
| Mode connexion | Réseau |

---


## 2. Accès Serveur NUC

### Adresse serveur

| Paramètre | Valeur |
|------------|--------|
| Adresse IP serveur | `192.168.1.3` |
| Nom DNS | `nuc.local` `www.nuc.local` |
|  | `dashboard.local` `www.dashboard.local` |
| Port SSH | `22` |

### Identifiants SSH

| Paramètre | Valeur |
|------------|--------|
| Login SSH | `etuXX` |
| Mot de passe SSH | |
| Dossier personnel | `/home/etuXX/` |

### Accès VS Code (Remote SSH)

| Paramètre | Valeur |
|------------|--------|
| Commande de connexion | `ssh -A etuXX@192.168.1.3` |
| Mot de passe | idem SSH |

## 3. Configuration MQTT

### Broker Mosquitto

| Paramètre | Valeur |
|------------|--------|
| Adresse broker | `192.168.1.3` |
| Port MQTT | `1883` |

### Identifiants MQTT

| Paramètre | Valeur |
|------------|--------|
| Username | `nuc` |
| Password | `nuc` |
| QoS utilisé | 0 / 1 / 2 |

### Topics attribués

| Usage | Topic | Payload |
|-------|-------|-------|
| Status événement | `robot3/events` | {"event": event_type, "timestamp": timestamp, "data": data} |
| message2 |  | |
| message3 |  | |

---

## 4. Base de données SQL

### Connexion

| Paramètre | Valeur |
|------------|--------|
| Type BDD | MySQL / MariaDB |
| Adresse serveur BDD | `192.168.1.3` |
| Port | `3306` |

### Identifiants BDD

| Paramètre | Valeur |
|------------|--------|
| Username | `robot1` |
| Password | robot1pass |
| Nom base | `robot1` |
| Table principale | `events` |

---

## 5. API Flask Robot

| Paramètre | Valeur |
|------------|--------|
| URL API | `http://192.168.1.1X:3000` |
| Port | 3000 |

### Liste endpoints

| Endpoint | URI | HTTP Verb | Paramètres |
|------------|--------|--------|--------|
| Blink ring | `/color` | `POST` | {"color": "green"} |
| Endpoint état | `/status` | `GET` | |

---

## 6. Grafana

| Paramètre | Valeur |
|------------|--------|
| URL Grafana | `http://192.168.1.XXX:300X` |
| Username | `etuXX` |
| Password | |
| Dashboard assigné | `Robot_XX` |

---

## 7. Vérifications en début de TP

| Test | Résultat |
|------|----------|
| Connexion SSH | OK / KO |
| Ping robot | OK / KO |
| Connexion MQTT | OK / KO |
| Connexion BDD | OK / KO |
| Accès API | OK / KO |
| Accès Grafana | OK / KO |

---

## 8. Bonnes pratiques

- Ne pas modifier les identifiants d'un autre étudiant
- Ne pas publier sur un topic non attribué
- Ne pas supprimer de tables SQL
- Ne pas arrêter les containers globaux
