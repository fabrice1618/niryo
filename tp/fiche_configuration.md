Parfait ✅  
Voici une **fiche de configuration individuelle prête à distribuer aux étudiants**.

Elle est conçue pour :

- ✅ éviter les erreurs de configuration  
- ✅ isoler chaque étudiant (comptes distincts)  
- ✅ centraliser tous les paramètres personnalisés  
- ✅ servir de référence tout au long du TP  

---

# 📄 FICHE DE CONFIGURATION INDIVIDUELLE  
## TP Robot Niryo Ned2 – Architecture MQTT / API / SQL / Grafana

---

## 👤 Informations étudiant

| Élément | Valeur |
|----------|--------|
| Groupe | |
| Numéro robot attribué | robotX |

---

# 🖥️ 1️⃣ Accès Serveur NUC

## 📡 Adresse serveur

| Paramètre | Valeur |
|------------|--------|
| Adresse IP serveur | `192.168.1.3` |
| Nom DNS (si utilisé) | `nuc.local` |
| Port SSH | `22` |

---

## 🔐 Identifiants SSH

| Paramètre | Valeur |
|------------|--------|
| Login SSH | `etuXX` |
| Mot de passe SSH | |
| Dossier personnel | `/home/etuXX/` |

---

## 🔐 VsCode remote SSH

| Paramètre | Valeur |
|------------|--------|
| Remote SSH | `ssh -A etuXX@192.168.1.3` |
| Mot de passe SSH | idem SSH |

---


## 🐳 Accès Docker

| Paramètre | Valeur |
|------------|--------|
| Autorisation Docker | ✅ Oui / ☐ Non |
| Nom réseau Docker | `robot_net` |
| Nom container MQTT handler | `mqtt_handler_XX` |
| Nom container API Flask | `api_robot_XX` |
| Nom container Grafana | `grafana_XX` |

---

# 🤖 2️⃣ Robot Niryo Ned2

| Paramètre | Valeur |
|------------|--------|
| IP Robot | `192.168.1.1XX` |
| Nom robot | `ned2_XX` |
| Port API robot | `9090` |
| Mode connexion | Directe / Réseau |

---

# 📡 3️⃣ Configuration MQTT

## 🛰 Broker Mosquitto

| Paramètre | Valeur |
|------------|--------|
| Adresse broker | `192.168.1.3` |
| Port MQTT | `1883` |
| Port MQTT sécurisé (si utilisé) | `8883` |

---

## 🔐 Identifiants MQTT

| Paramètre | Valeur |
|------------|--------|
| Username | `robotXX` |
| Password | |
| QoS utilisé | 0 / 1 / 2 |

---

## 📌 Topics attribués

| Usage | Topic |
|-------|-------|
| Commande mouvement | `robotXX/cmd/move` |
| Etat robot | `robotXX/state` |
| Logs | `robotXX/log` |

---

# 🗄 4️⃣ Base de Données SQL

## 📡 Connexion

| Paramètre | Valeur |
|------------|--------|
| Type BDD | MySQL / MariaDB / PostgreSQL |
| Adresse serveur BDD | `192.168.1.XXX` |
| Port | `3306` / `5432` |
| Nom base | `robotXX_db` |

---

## 🔐 Identifiants BDD

| Paramètre | Valeur |
|------------|--------|
| Username | `robotXX` |
| Password | |
| Table principale | `robot_moves` |

---

# 🌐 5️⃣ API Flask

| Paramètre | Valeur |
|------------|--------|
| URL API | `http://192.168.1.XXX:50XX` |
| Port | |
| Endpoint principal | `/move` |
| Endpoint état | `/status` |

---

# 📊 6️⃣ Grafana

| Paramètre | Valeur |
|------------|--------|
| URL Grafana | `http://192.168.1.XXX:300X` |
| Username | `etuXX` |
| Password | |
| Dashboard assigné | `Robot_XX` |

---

# 🔁 7️⃣ Schéma de communication personnalisé

```
PC étudiant
   ↓ HTTP
API Flask (port 50XX)
   ↓ MQTT publish
Broker Mosquitto
   ↓ MQTT subscribe
Handler Python
   ↓
Robot Niryo
   ↓
Base SQL
   ↓
Grafana
```

---

# ✅ 8️⃣ Vérifications à effectuer en début de TP

| Test | Résultat |
|------|----------|
| Connexion SSH | ✅ / ❌ |
| Ping robot | ✅ / ❌ |
| Connexion MQTT | ✅ / ❌ |
| Connexion BDD | ✅ / ❌ |
| Accès API | ✅ / ❌ |
| Accès Grafana | ✅ / ❌ |

---

# 🔒 9️⃣ Bonnes pratiques

- Ne pas modifier les identifiants d’un autre étudiant
- Ne pas publier sur un topic non attribué
- Ne pas supprimer de tables SQL
- Ne pas arrêter les containers globaux

---

# 🎯 Option enseignant (organisation conseillée)

Pour 12 étudiants :

| Étudiant | Topic | DB | Port API | Port Grafana |
|----------|--------|--------|------------|-------------|
| 01 | robot01 | robot01_db | 5001 | 3001 |
| 02 | robot02 | robot02_db | 5002 | 3002 |
| … | … | … | … | … |

→ Isolation complète  
→ Aucun conflit réseau  
→ Facilité de debugging  

---

# 💡 Bonus : Version prête à imprimer

Si tu veux, je peux te générer :

- ✅ une version PDF propre prête à distribuer
- ✅ une version avec génération automatique des comptes
- ✅ un tableau Excel générateur d’identifiants
- ✅ un script Bash pour créer tous les comptes automatiquement

Tu as combien d’étudiants dans le groupe ?