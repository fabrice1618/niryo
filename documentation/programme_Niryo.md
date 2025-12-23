# Programme de cours: Infrastructure client / serveur dans un contexte industriel

## Informations générales

**Département :** Technique & Nucléaire  
**Formation :** B3 D&P  
**Option :** Processus Numérique 4.0 (PN4.0)  
**Module :** *Infrastructure client / serveur dans un contexte industriel*  
**Thématique :** Technologie 4.0 – Informatique  

**Intervenant :** Fabrice Guichard  
**Responsable pédagogique :** Christian Skarniak  
**Référent pédagogique :** Sébastien Arnaud  

**Dernière modification :** 27/11/2025

## Objectifs pédagogiques

- Mettre en réseau un robot Niryo avec un poste client  
- Programmer des mouvements et séquences en Python  
- Connecter un capteur externe simple au robot ou à un microcontrôleur  
- Faire remonter des données vers un mini-serveur / dashboard web  
- Concevoir une supervision légère (Node‑RED / Grafana / Flask)  
- Réaliser une mini‑application industrielle robot + supervision  



## Méthodes pédagogiques

- Cours magistral  
- Travaux pratiques guidés  
- Projet final supervisé  

## Matériel / Logiciels nécessaires

- Robot Niryo  
- Microcontrôleur (type ESP32/Arduino si besoin)  
- PC avec Python + SDK Niryo  
- Outils : Node‑RED, Grafana, Flask (selon les TP)


## Répartition horaire

| Activité | Durée |
|---------|-------|
| Cours magistral | 3,5 h |
| TD | 0 h |
| Travaux pratiques | 14 h |
| Test / Soutenance | 3,5 h |
| Travail en autonomie | 0 h |
| **Total** | **21 h** |


## Séance 01 – Cours magistral (3,5 h)
### *Découverte infrastructure + réseau basique*

- Prise en main du robot Niryo  
- Notions d’IP / connexion réseau  
- Test de communication PC ↔ Niryo  
- Introduction au SDK Python  



## Séance 02 – Travaux pratiques (3,5 h)
### *Python & mouvement robotique*

- Scripts simples : déplacement / vitesse / trajectoire  
- Calibration, prise d’objet, scénario automatique  
- **TP : programme de cycle robotisé simple**



## Séance 03 – Travaux pratiques (3,5 h)
### *Capteurs externes & I/O robot*

- Lecture d’un capteur (fin de course, température, distance…)  
- Intégration microcontrôleur (option)  
- Déclenchement d’un mouvement sur événement  



## Séance 04 – Travaux pratiques (3,5 h)
### *Client‑serveur léger avec Python*

- Mini‑API Flask ou WebSocket pour piloter le robot  
- Commandes réseau : start / stop / sequence  
- **TP : contrôleur web (boutons) → action robot**



## Séance 05 – Travaux pratiques (3,5 h)
### *Supervision & visualisation*

- Dashboard Node‑RED ou Grafana  
- Affichage positions / états capteurs / logs  
- Mise en place d’alarmes simples  



## Séance 06 – Test / Projet final (3,5 h)
### *Projet de synthèse & soutenance*

Chaque groupe réalise un **poste industriel minimal** :

➡️ capteur → décision → mouvement robot → monitoring  
➡️ démonstration + oral + dépôt du code final  

