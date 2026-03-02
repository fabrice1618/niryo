#!/usr/bin/env python3
"""Outil de diagnostic API — TP Niryo"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import requests

# Charger .env racine
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# Lire config
diag_api = os.getenv("DIAG_API_HOST", "localhost")
diag_port = int(os.getenv("DIAG_API_PORT", 3000))

BASE_URL = f"http://{diag_api}:{diag_port}"

VALID_COLORS = ["red", "green", "blue"]


def afficher_config():
    print("=" * 40)
    print("  Diagnostic API — TP Niryo")
    print("=" * 40)
    print(f"  URL      : {BASE_URL}")
    print("=" * 40)


def envoyer_couleur(color):
    url = f"{BASE_URL}/color"
    payload = {"color": color}
    print(f"\nRequête POST {url}")
    print(f"  Body : {json.dumps(payload)}")
    try:
        r = requests.post(url, json=payload, timeout=10)
    except requests.ConnectionError:
        print(f"\nErreur : impossible de se connecter à {BASE_URL}")
        print("Vérifiez que le robot (ou mock) est démarré.")
        sys.exit(1)
    except requests.Timeout:
        print(f"\nErreur : timeout (pas de réponse après 10s)")
        sys.exit(1)

    print(f"\nRéponse HTTP {r.status_code} :")
    try:
        print(f"  {json.dumps(r.json(), indent=2)}")
    except ValueError:
        print(f"  {r.text}")


def main():
    afficher_config()

    # Choix de la couleur
    print("\nCouleur à envoyer :")
    for i, c in enumerate(VALID_COLORS, 1):
        print(f"  {i}. {c}")
    print(f"  4. Saisie libre (test erreur)")

    choix = input("Choix [1/2/3/4] : ").strip()

    if choix in ("1", "2", "3"):
        color = VALID_COLORS[int(choix) - 1]
    elif choix == "4":
        color = input("Couleur : ").strip()
        if not color:
            print("Saisie vide, abandon.")
            sys.exit(1)
    else:
        print("Choix invalide.")
        sys.exit(1)

    envoyer_couleur(color)


if __name__ == "__main__":
    main()
