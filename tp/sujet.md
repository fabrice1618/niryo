Merci pour le synoptique ✅  
Je te propose un **TP progressif structuré**, adapté à un contexte BUT / BTS / Licence Pro / école d’ingénieur, permettant de mettre en œuvre **tous les éléments du schéma** :

- Robot **Niryo Ned2**
- Client MQTT
- Broker Mosquitto
- Handler Python (Docker)
- Base SQL
- API Flask
- Dashboard Grafana
- Communication HTTP
- Communication MQTT

L’objectif est de construire **progressivement une architecture IIoT complète** autour du robot.

---

# 🎯 Objectif global du TP

Mettre en œuvre une architecture distribuée permettant :

- ✅ le pilotage d’un robot Niryo Ned2
- ✅ la transmission d’ordres via MQTT
- ✅ le traitement des messages en Python
- ✅ le stockage en base SQL
- ✅ la supervision via Grafana
- ✅ le pilotage via une API Flask

---

# 🧭 Organisation pédagogique

## Durée conseillée
4 à 6 séances de 2h à 3h

## Compétences visées

- Architecture client/serveur
- Communication MQTT
- API REST
- Conteneurisation Docker
- Base de données SQL
- Supervision industrielle
- Robotique collaborative

---

# 🧩 Progression pédagogique

---

# 🟢 Séance 1 — Prise en main du robot Niryo Ned2

## 🎯 Objectifs

- Comprendre le fonctionnement du robot
- Tester les scripts fournis
- Découvrir l’API Python du Niryo

## 🔎 Activités

1. Connexion au robot
2. Exécution d’un script simple :
   - Homing
   - Déplacement en coordonnées cartésiennes
   - Ouverture/fermeture pince
3. Création d’un petit scénario :
   - Pick & Place simple

## ✅ Compétences validées

- Connexion robot
- Lancement de scripts
- Compréhension des axes et coordonnées

---

# 🟡 Séance 2 — Introduction à MQTT

## 🎯 Objectifs

- Comprendre le principe publish/subscribe
- Tester le broker Mosquitto
- Envoyer des ordres au robot via MQTT

---

## 📚 Rappel théorique

Schéma :

Client → Broker → Subscriber

Topic utilisé :
```
robot1/position
```

Message exemple :
```json
{ "x": 100, "y": 200, "z": 150 }
```

---

## 🔎 Activités

1. Test manuel avec un client MQTT :
   - Publication d’un message
2. Observation du handler Python
3. Vérification que le robot exécute la commande

---

## ✅ Compétences validées

- Comprendre un broker
- Publier un message
- Lire un message JSON

---

# 🟠 Séance 3 — Handler Python + Base SQL

## 🎯 Objectifs

- Comprendre le rôle du conteneur Docker
- Analyser le script de handler
- Stocker les ordres en base SQL

---

## 🔎 Activités

1. Observer le container Docker
2. Comprendre :
   - Souscription au topic
   - Décodage JSON
   - Insertion SQL
3. Vérifier en base :
   - timestamp
   - coordonnées
   - état d’exécution

---

## ✅ Compétences validées

- Docker (niveau compréhension)
- SQL (INSERT / SELECT)
- Traçabilité industrielle

---

# 🔵 Séance 4 — API Flask de pilotage

## 🎯 Objectifs

- Comprendre le rôle d’une API REST
- Envoyer des commandes HTTP
- Faire le lien HTTP → MQTT → Robot

---

## 🔎 Activités

1. Analyse de l’API Flask :
   - Endpoint `/move`
2. Test via navigateur ou Postman
3. Observer la chaîne complète :

```
HTTP → Flask → MQTT → Handler → Robot → SQL
```

---

## ✅ Compétences validées

- Requête HTTP
- Architecture multi-couches
- Compréhension middleware

---

# 🟣 Séance 5 — Supervision avec Grafana

## 🎯 Objectifs

- Visualiser les données SQL
- Créer un dashboard de suivi robot

---

## 🔎 Activités

1. Connexion Grafana à la base SQL
2. Création de graphiques :
   - Nombre de mouvements
   - Répartition des positions
   - Temps d’exécution
3. Ajout d’un indicateur d’état

---

## ✅ Compétences validées

- Supervision industrielle
- Lecture de données temps réel
- Indicateurs de performance

---

# 🔴 Séance 6 — TP Final : Scénario industriel complet

## 🎯 Mise en situation

Vous devez mettre en place une cellule robotisée pilotable à distance permettant :

- 📦 Prise d’un objet
- 📤 Dépose en zone définie
- 📊 Enregistrement des mouvements
- 📈 Supervision temps réel

---

## 📝 Travail demandé

1. Créer un scénario de pick & place automatisé
2. Le piloter via :
   - MQTT direct
   - API HTTP
3. Vérifier l’enregistrement en base
4. Créer un dashboard de suivi
5. Analyser :
   - latence
   - fiabilité
   - traçabilité

---

# 📊 Vue globale de la progression

| Séance | Niveau | Technologie | Complexité |
|--------|--------|------------|------------|
| 1 | Robot seul | Niryo | 🟢 |
| 2 | Communication | MQTT | 🟡 |
| 3 | Middleware | Python + SQL | 🟠 |
| 4 | API | Flask | 🔵 |
| 5 | Supervision | Grafana | 🟣 |
| 6 | Intégration | Full stack | 🔴 |

---

# 🧠 Logique pédagogique

La progression respecte :

1. ✅ Concret → Abstrait
2. ✅ Local → Distribué
3. ✅ Mono-système → Architecture complète
4. ✅ Exécution → Traçabilité → Supervision

On part du robot physique pour arriver à une architecture industrielle IIoT complète.

---

# 💡 Option avancée (si niveau ingénieur)

- Ajout gestion d’erreurs
- QoS MQTT
- Sécurisation (authentification broker)
- Gestion multi-robots
- Analyse statistique des données

---

Si tu veux, je peux aussi te fournir :

- ✅ une version prête à distribuer aux étudiants (format PDF structuré)
- ✅ une version enseignant avec corrigé pédagogique
- ✅ une grille d’évaluation par compétences
- ✅ une version adaptée BUT GEII / BTS CRSA / Licence Pro / Ingénieur  

Tu es sur quel niveau de formation ?