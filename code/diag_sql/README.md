# Diagnostic SQL — TP Niryo

Outil interactif pour interroger la base de données MySQL du robot.
Équivalent de `diag_mqtt` et `diag_api` mais pour les requêtes SQL.

## Ce que fait l'outil

- Affiche la configuration MySQL en cours (hôte, port, base, utilisateur)
- Teste la connexion à la base de données
- Propose un menu de requêtes prédéfinies (événements récents, comptage, erreurs)
- Permet la saisie libre pour exécuter n'importe quelle requête SQL
- Affiche les résultats sous forme de tableau formaté

## Installation

```bash
cd code/diag_sql
pip install pymysql python-dotenv
```

## Utilisation

```bash
python3 diag_sql.py
```

Exemple de session :

```
========================================
  Diagnostic SQL — TP Niryo
========================================
  Host     : localhost
  Port     : 3306
  User     : robot3
  Password : robot3pass
  Database : robot3
========================================

Connexion MySQL établie.

Requête à exécuter :
  1. Afficher tous les événements (10 derniers)
  2. Compter les événements par type
  3. Afficher les erreurs uniquement
  4. Événements des 10 dernières minutes
  5. Saisie libre (requête SQL)
Choix [1/2/3/4/5] : 2

> SELECT event_type, COUNT(*) AS nb FROM events GROUP BY event_type;

+-------------+----+
| event_type  | nb |
+-------------+----+
| color_done  | 5  |
| color_error | 2  |
+-------------+----+

2 ligne(s) retournée(s).
```

## Configuration

L'outil lit le fichier `.env` à la racine du projet :

```ini
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=robot3
MYSQL_PASSWORD=robot3pass
MYSQL_DATABASE=robot3
```

> **Note** : ces paramètres sont les mêmes que ceux utilisés par `event_handler.py`. Si le handler fonctionne, `diag_sql` fonctionnera aussi.
