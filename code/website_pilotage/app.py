#!/usr/bin/env python3
"""
Site web de pilotage du robot Niryo — TP Niryo
Interface web pour envoyer des commandes couleur au robot via l'API Flask.
"""

import os
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
import requests

# Charger .env racine (même pattern que les autres outils)
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

# --- Logging ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Configuration ---------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser(description="Site web de pilotage du robot Niryo")
    parser.add_argument(
        '--robot-ip',
        help="IP du robot réel (override de API_HOST dans .env)"
    )
    return parser.parse_args()


def sanitize_host(host):
    """0.0.0.0 est une adresse de bind serveur, côté client on utilise localhost."""
    return "localhost" if host == "0.0.0.0" else host


def build_targets(args):
    """Construit le dictionnaire des cibles robot depuis .env et arguments CLI."""
    # Cible mock : toujours depuis .env
    mock_host = sanitize_host(os.getenv("MOCK_API_HOST", "localhost"))
    mock_port = int(os.getenv("MOCK_API_PORT", 3000))

    # Cible robot réel : --robot-ip en priorité, sinon ROBOT_API depuis .env
    robot_host = args.robot_ip if args.robot_ip else sanitize_host(os.getenv("ROBOT_API", "192.168.1.11"))
    robot_port = int(os.getenv("ROBOT_PORT", 3000))

    return {
        "mock": f"http://{mock_host}:{mock_port}",
        "robot": f"http://{robot_host}:{robot_port}",
    }


# --- Flask App -------------------------------------------------------

app = Flask(__name__)
TARGETS = {}  # initialisé dans main()


@app.route('/')
def index():
    """Page principale avec les boutons de commande."""
    return render_template('index.html', targets=TARGETS)


@app.route('/send_color', methods=['POST'])
def send_color():
    """Proxy vers l'API robot : évite les problèmes CORS."""
    data = request.json
    if not data or "color" not in data:
        return jsonify({"error": 'Champ "color" manquant'}), 400

    # Résoudre la cible depuis la clé envoyée par le frontend
    target_key = data.get("target", "mock")
    base_url = TARGETS.get(target_key)
    if not base_url:
        return jsonify({"error": f"Cible inconnue : {target_key}"}), 400

    url = f"{base_url}/color"
    try:
        resp = requests.post(url, json={"color": data["color"]}, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except requests.ConnectionError:
        logger.error(f"Impossible de joindre le robot à {url}")
        return jsonify({"error": f"Robot non joignable à {base_url}"}), 502
    except requests.Timeout:
        logger.error(f"Timeout en contactant {url}")
        return jsonify({"error": "Timeout : le robot ne répond pas"}), 504


# --- Main ------------------------------------------------------------

if __name__ == '__main__':
    args = parse_args()
    TARGETS = build_targets(args)

    logger.info(f"Cible mock  : {TARGETS['mock']}")
    logger.info(f"Cible robot : {TARGETS['robot']}")
    logger.info("Site web démarré sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
