Voici **un programme de cours structuré et adapté** à un **TP réseaux TCP/IP** utilisant des **robots Niryo** et des **micro‑contrôleurs M5Stack**, en lien direct avec l’architecture réseau illustrée dans votre schéma.

------------------------------------

### 🧭 Objectif général du module
Permettre aux étudiants de comprendre et manipuler les **principes fondamentaux des réseaux TCP/IP** (adressage IP, réseau, routage, DHCP, adressage statique), puis de les appliquer dans un environnement concret :
- Micro‑contrôleurs **M5Stack** connectés en WiFi via un AP étudiant  
- Robots **Niryo Ned / Ned2** en **IP statique**  
- Serveur NUC local  
- Routeurs indépendants pour isoler et contrôler les flux  

------------------------------------

## ### 📘 Plan de cours complet (8 séances de 2h)

---

## ### **Séance 1 — Introduction aux réseaux TCP/IP**
**Objectifs :**
- Comprendre ce qu’est un réseau, Internet, un LAN, WLAN.
- Notion de communication IP, modèle TCP/IP vs OSI.

**Contenu :**
- Paquet, trame, adresse MAC, IP, port, protocole.
- Ping, ARP, ICMP.

**Mini‑TP :**
- Ping entre postes étudiants  
- Observation ARP : `arp -a`  
- Tester la connectivité via l’AP étudiant

---

## ### **Séance 2 — Adressage IPv4 : structure et calculs**
**Objectifs :**
- Comprendre une adresse IPv4 (ex : 192.168.1.x)
- Calculer : réseau, masque, broadcast, plage d’hôtes

**Contenu :**
- Masques (ex : /24, /16…)
- Classes, mais surtout CIDR moderne
- Notion de sous-réseaux (ex : séparation LAN robots / LAN étudiants)

**Mini‑TP :**
- Calcul du réseau robot : 192.168.1.0/24  
- Identifier :  
  • IP routeur robot  
  • IP serveur NUC (192.168.1.2)  
  • IP fixes robots (192.168.1.11 → .15)  

---

## ### **Séance 3 — DHCP vs IP statique**
**Objectifs :**
- Comprendre l’intérêt du DHCP pour les M5Stack (mobilité)
- Comprendre pourquoi les robots Niryo ont une IP fixe

**Contenu :**
- Fonctionnement DHCP (Discover / Offer / Request / Ack)
- Avantages / limites
- Exemple : plage DHCP du routeur robot

**Mini‑TP :**
- Observer l’IP reçue par un M5Stack  
- Comparer configuration IP dynamique vs statique sur PC étudiant  
- Définir une IP statique sur un poste pour contacter un robot Niryo  

---

## ### **Séance 4 — Notion de routage et rôle des routeurs**
**Objectifs :**
- Comprendre pourquoi chaque zone réseau a son routeur
- Lire le schéma : AP étudiants → Routeur LAN robot → Switch → NUC/robots

**Contenu :**
- Table de routage : `route -n`
- Gateway, interface, métrique
- Isolation réseau : LAN étudiant vs LAN robot

**Mini‑TP :**
- Lire la table de routage du PC et du M5Stack  
- Vérifier que les flux vers robots passent par le routeur LAN robot  
- Ping inter-sous-réseaux si autorisé  

---

## ### **Séance 5 — WiFi et couche 2 : AP étudiants et réseau robot**
**Objectifs :**
- Comprendre l’infrastructure WiFi et les différents SSID
- Comprendre l’importance du Layer‑2 switch pour les robots

**Contenu :**
- SSID, authentification WPA2/3
- DHCP côté AP étudiants vs LAN robot
- Switch L2 = pas de routage

**Mini‑TP :**
- Connexion d’un M5Stack au SSID étudiant  
- Relever l'adresse IP dynamique  
- Vérifier la connectivité jusqu’au routeur robot (traceroute)  

---

## ### **Séance 6 — TP Robot Niryo : communication IP**
**Objectifs :**
- Comprendre la communication avec un robot en IP fixe

**Contenu :**
- API Niryo (HTTP/TCP suivant version)
- Adresse robot : ex. 192.168.1.11
- Rôle du serveur NUC (192.168.1.2)

**TP pratique :**
- Ping du robot  
- Requête API simple depuis Python (ou Node-RED si disponible)  
- Vérifier la cohérence du sous-réseau  

---

## ### **Séance 7 — TP M5Stack : sockets TCP/UDP**
**Objectifs :**
- Comprendre la communication TCP/UDP depuis un micro‑contrôleur

**Contenu :**
- Programmation d’un client TCP simple
- Envoi capteurs M5Stack → serveur NUC

**TP :**
- Wifi.begin + DHCP  
- Création d’un client TCP qui envoie un message au NUC  
- Le NUC renvoie un ACK → affiché sur l’écran M5Stack  

---

## ### **Séance 8 — TP intégrateur : flux M5Stack → serveur → robot**
**Objectif :**  
Créer une application complète utilisant l’infrastructure réseau.

**Scénarios possibles :**
- Un M5Stack envoie une commande au serveur NUC  
- Le NUC interprète la commande  
- Le NUC envoie une instruction au robot Niryo (ex : déplacer un axe)

**Réseau mobilisé :**
- M5Stack → WiFi étudiant → Routeur LAN robot → NUC → Robot Niryo

**Étudiant doit vérifier :**
- Bonne IP du M5Stack (DHCP)  
- Route vers le LAN robot  
- IP statique du robot  
- API fonctionnelle  

------------------------------------

## ### 📑 Synthèse du programme

**Notions générales :**
- TCP/IP  
- IPv4 (réseau, masque, broadcast)  
- Routage, gateway  
- DHCP et IP statique  
- WiFi et switch L2  

**Application pratique (votre architecture) :**
- AP étudiants → IP dynamique pour M5Stack  
- Routeur robot → réseau 192.168.1.0/24  
- Robots Niryo en IP fixe  
- NUC comme serveur pivot  

------------------------------------

Si vous voulez, je peux aussi vous fournir :
- un **document PDF** complet de cours,
- les **fiches TP détaillées**,
- des **scripts Python prêts à l’emploi** pour Niryo et M5Stack,
- ou un **schéma réseau retravaillé propre**.