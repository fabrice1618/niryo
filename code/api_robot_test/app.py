#!/usr/bin/env python3
"""
API Flask mock simulant le comportement de l'API de contrôle du robot Niryo.
Permet de tester les interfaces web et les clients API sans connexion physique au robot.
"""

import os
import time
import random
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import logging

# Charger les variables d'environnement
load_dotenv()

# Configuration Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Support des caractères UTF-8

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def log_request(endpoint, params, result):
    """
    Log chaque requête avec timestamp, endpoint, paramètres et résultat.

    Args:
        endpoint: Nom de l'endpoint appelé
        params: Paramètres de la requête
        result: Résultat (succès/erreur)
    """
    logger.info(f"Endpoint: {endpoint} | Params: {params} | Result: {result}")


@app.route('/autocalibrate', methods=['POST'])
def autocalibrate():
    """
    Simule la calibration automatique du robot.
    Délai: 2-3 secondes
    """
    start_time = time.time()

    # Simulation du délai de calibration (2-3 secondes)
    delay = random.uniform(2.0, 3.0)
    time.sleep(delay)

    duration = round(time.time() - start_time, 2)

    response = {
        "status": "success",
        "message": "Calibration automatique terminée",
        "duration": duration
    }

    log_request('/autocalibrate', {}, 'success')

    return jsonify(response), 200


@app.route('/color/red', methods=['POST'])
def color_red():
    """
    Simule le clignotement du LED ring en rouge.
    Délai: 3-4 secondes
    """
    # Simulation du délai de séquence (3-4 secondes)
    delay = random.uniform(3.0, 4.0)
    time.sleep(delay)

    response = {
        "status": "success",
        "message": "Séquence rouge exécutée",
        "color": "red"
    }

    log_request('/color/red', {}, 'success')

    return jsonify(response), 200


@app.route('/color/blue', methods=['POST'])
def color_blue():
    """
    Simule le clignotement du LED ring en bleu.
    Délai: 3-4 secondes
    """
    # Simulation du délai de séquence (3-4 secondes)
    delay = random.uniform(3.0, 4.0)
    time.sleep(delay)

    response = {
        "status": "success",
        "message": "Séquence bleue exécutée",
        "color": "blue"
    }

    log_request('/color/blue', {}, 'success')

    return jsonify(response), 200


@app.route('/color/green', methods=['POST'])
def color_green():
    """
    Simule le clignotement du LED ring en vert.
    Délai: 3-4 secondes
    """
    # Simulation du délai de séquence (3-4 secondes)
    delay = random.uniform(3.0, 4.0)
    time.sleep(delay)

    response = {
        "status": "success",
        "message": "Séquence verte exécutée",
        "color": "green"
    }

    log_request('/color/green', {}, 'success')

    return jsonify(response), 200


@app.route('/status', methods=['GET'])
def status():
    """
    Retourne l'état actuel du robot simulé.
    Délai: < 100ms (immédiat)
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    response = {
        "timestamp": timestamp
    }

    log_request('/status', {}, 'success')

    return jsonify(response), 200


@app.errorhandler(404)
def not_found(error):
    """Gestion des endpoints non trouvés"""
    return jsonify({
        "status": "error",
        "message": "Endpoint non trouvé"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Gestion des méthodes HTTP non autorisées"""
    return jsonify({
        "status": "error",
        "message": "Méthode HTTP non autorisée"
    }), 405


if __name__ == '__main__':
    # Récupération des variables d'environnement
    host = os.getenv('API_TEST_HOST', '0.0.0.0')
    port = int(os.getenv('API_TEST_PORT', 3000))
    debug = os.getenv('API_TEST_DEBUG', 'True').lower() == 'true'

    logger.info(f"Démarrage de l'API Robot Test Mock")
    logger.info(f"Host: {host}")
    logger.info(f"Port: {port}")
    logger.info(f"Debug: {debug}")

    app.run(host=host, port=port, debug=debug)
