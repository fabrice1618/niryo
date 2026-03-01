#!/usr/bin/env python3
"""Outil de diagnostic SQL — TP Niryo"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import pymysql

# Charger .env racine
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Lire config
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "robot3")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "robot3pass")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "robot3")


def afficher_config():
    print("=" * 40)
    print("  Diagnostic SQL — TP Niryo")
    print("=" * 40)
    print(f"  Host     : {MYSQL_HOST}")
    print(f"  Port     : {MYSQL_PORT}")
    print(f"  User     : {MYSQL_USER}")
    print(f"  Password : {MYSQL_PASSWORD}")
    print(f"  Database : {MYSQL_DATABASE}")
    print("=" * 40)


def connecter():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset="utf8mb4",
        )
        print("\nConnexion MySQL établie.")
        return conn
    except pymysql.err.OperationalError as e:
        print(f"\nErreur de connexion MySQL : {e}")
        print("Vérifiez que MySQL est démarré et que les identifiants sont corrects.")
        sys.exit(1)


def afficher_resultats(cursor):
    colonnes = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        print("\n(aucun résultat)")
        return

    # Calculer les largeurs de colonnes
    largeurs = [len(c) for c in colonnes]
    for row in rows:
        for i, val in enumerate(row):
            largeurs[i] = max(largeurs[i], len(str(val)))

    # Afficher l'en-tête
    sep = "+-" + "-+-".join("-" * l for l in largeurs) + "-+"
    header = "| " + " | ".join(c.ljust(l) for c, l in zip(colonnes, largeurs)) + " |"
    print(f"\n{sep}")
    print(header)
    print(sep)

    # Afficher les lignes
    for row in rows:
        ligne = "| " + " | ".join(str(v).ljust(l) for v, l in zip(row, largeurs)) + " |"
        print(ligne)
    print(sep)
    print(f"\n{len(rows)} ligne(s) retournée(s).")


def main():
    afficher_config()
    conn = connecter()

    # Choix de la requête
    print("\nRequête à exécuter :")
    print("  1. Afficher tous les événements (10 derniers)")
    print("  2. Compter les événements par type")
    print("  3. Afficher les erreurs uniquement")
    print("  4. Événements des 10 dernières minutes")
    print("  5. Saisie libre (requête SQL)")

    choix = input("Choix [1/2/3/4/5] : ").strip()

    requetes = {
        "1": "SELECT * FROM events ORDER BY timestamp DESC LIMIT 10;",
        "2": "SELECT event_type, COUNT(*) AS nb FROM events GROUP BY event_type;",
        "3": "SELECT timestamp, color FROM events WHERE event_type = 'color_error' ORDER BY timestamp DESC;",
        "4": "SELECT * FROM events WHERE timestamp > NOW() - INTERVAL 10 MINUTE ORDER BY timestamp DESC;",
    }

    if choix in requetes:
        requete = requetes[choix]
    elif choix == "5":
        requete = input("Requête SQL : ").strip()
        if not requete:
            print("Saisie vide, abandon.")
            conn.close()
            sys.exit(1)
    else:
        print("Choix invalide.")
        conn.close()
        sys.exit(1)

    print(f"\n> {requete}")

    try:
        cursor = conn.cursor()
        cursor.execute(requete)
        afficher_resultats(cursor)
    except pymysql.err.ProgrammingError as e:
        print(f"\nErreur SQL : {e}")
    except pymysql.err.OperationalError as e:
        print(f"\nErreur opérationnelle : {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
