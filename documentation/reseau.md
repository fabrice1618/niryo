# 🎓 Programme de cours : “Configuration d’un réseau robotique & IoT distribué”

---

## Objectifs:

- configurer un LAN complet (robots, serveurs, capteurs)  
- comprendre et diagnostiquer le réseau  
- déployer un broker MQTT  
- orchestrer des services Docker  
- écrire des micro‑services Python MQTT  
- commander un robot via une API web  
- visualiser le système en temps réel via Grafana / Node‑RED  


## Module 1 — Bases indispensables en Réseau (fondations)
Objectif : que tous les étudiants puissent lire, diagnostiquer et configurer un réseau local.

**Notions à couvrir :**
- Qu’est‑ce qu’un réseau ?  
- Différences LAN / WAN / WLAN  
- Paquets, trames, switch, routeur  
- Adresse MAC  
- IPv4 :  
  - Adresse, masque, calcul de réseau  
  - Passerelle, DNS  
- DHCP vs IP statique  
- Ping, traceroute, arp  
- Ports TCP/UDP (1883, 1880, 3000, 5000…)  
- Pare‑feu local (UFW)

**TP :**
- Configurer une machine en IP statique  
- Déterminer l’IP d’un robot Niryo  
- Tester la connectivité entre les différents équipements (PC → MQTT → robot)

---

## Module 2 — Architecture du projet : vue d’ensemble du système
Objectif : comprendre le schéma et le rôle de chaque élément.

**Contenu :**
- Présentation du diagramme système  
- Rôle du switch, routeur, serveur NUC  
- Robots Niryo → flux MQTT  
- Microcontrôleurs/Capteurs → messages MQTT  
- Serveur NUC → Brokers, API, Backends, Base SQL, Dashboards  
- Communication des services via MQTT et HTTP

**TP :**
- Reconstituer l’architecture sur papier  
- Identifier tous les points d’entrée/sortie réseau  
- Cartographier les ports utilisés

---

## Module 3 — MQTT (Mosquitto) : comprendre, installer, configurer
Objectif : savoir mettre en place la colonne vertébrale du système.

**Contenu :**
- Qu’est‑ce qu’un broker MQTT ?  
- Topics, payloads, QoS  
- Souscription / publication  
- MQTT dans l’IoT et la robotique  
- Installation de Mosquitto (Linux / Docker)  
- Configuration de base :  
  - ports  
  - anonymous vs password  
  - fichiers de config

**TP :**
- Installer Mosquitto sur le serveur NUC  
- Publier et souscrire depuis un PC  
- Simuler un robot en envoyant des messages test

---

## Module 4 — Docker : isolation et déploiement des services
Objectif : déployer tous les services du schéma dans des conteneurs.

**Contenu :**
- Images, containers, volumes, networks  
- Docker Compose  
- Mise en place d’un réseau docker bridge  
- Gestion des ports (exposer 3000, 1880, 1883, 5000…)  
- Rebuild / logs / restart policies

**TP :**
- Déployer :  
  - Mosquitto  
  - Backend Python  
  - Flask API  
  - Dashboard Grafana  
  - Dashboard Node‑RED  
- Tester les connexions inter‑conteneurs

---

## Module 5 — API Python Flask pour pilotage robot
Objectif : mettre en place l’API permettant au reste du système de commander le robot.

**Contenu :**
- Fonctionnement REST : GET, POST  
- Création d’une API Flask simple  
- Appels vers PyNiryo et commandes au robot  
- Intégration MQTT (publication des états, réception d’ordres)

**TP :**
- Créer une API “/move”, “/calibrate”, “/status”  
- Conteneuriser l’API  
- Tester via Postman ou le navigateur

---

## Module 6 — Python “Message Handlers” : traitement et routage MQTT
Objectif : développer les micro‑services situés entre robots/capteurs ↔ base SQL ↔ dashboards.

**Contenu :**
- Connexion Paho MQTT  
- Lecture de topics capteurs (température, humidité, positions robots…)  
- Format JSON  
- Traitement et nettoyage des données  
- Écriture en base SQL  
- Publication d’événements vers d’autres topics

**TP :**
- Écrire un micro‑service “listener” MQTT  
- Stocker les données dans SQL  
- Générer un topic de monitoring robot

---

## Module 7 — Base de données SQL
Objectif : stocker l’historique des données du système.

**Contenu :**
- Tables, clés, index  
- CRUD (Create, Read, Update, Delete)  
- Connexion Python → SQL (SQLAlchemy ou PyMySQL)  
- Requêtes simples pour exporter les données des capteurs et robots  
- Accès depuis Grafana

**TP :**
- Créer une table `measurements`  
- Insérer automatiquement des données depuis le handler Python  
- Vérifier dans Grafana

---

## Module 8 — Dashboards (Grafana et Node‑RED)
Objectif : visualiser et commander le robot depuis l’interface.

### Grafana :
- Connexion base SQL  
- Création de graphiques  
- Représentation de la position robot, capteurs…

### Node‑RED :
- Node MQTT  
- Node UI (dashboard)  
- Boutons de commandes envoyant des messages vers l’API Flask ou MQTT

**TP :**
- Dashboard robot avec :  
  - historique positions  
  - interruptions  
  - capteurs IoT  
- Node‑RED : bouton “Start mission” qui envoie un ordre au robot

---

## Module 9 — Sécurité et bonnes pratiques
Objectif : sécuriser la plateforme.

**Contenu :**
- Utilisateurs Mosquitto  
- Mots de passe MQTT  
- Contrôle d’accès topics  
- Sécurité Docker (réseaux, isolation)  
- API tokens  
- Sauvegardes de la base SQL  
- Logs et supervision

**TP :**
- Activer l’authentification MQTT  
- Protéger l’API Flask par token  
- Créer un healthcheck Docker

---

## Module 10 — Projet final : déployer l’architecture complète
Chaque groupe configure tout le système :

1. Switch + routeur + IP statiques  
2. MQTT + micro‑services  
3. API Flask reliée aux robots  
4. Base SQL  
5. Dashboards  
6. Communication bidirectionnelle robot ↔ serveur ↔ dashboards



