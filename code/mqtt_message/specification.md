# MQTT message handler

## fonctions du script python

- se connecte au broker mosquitto avec utilisateur et mot de passe sur 1883
- abonnement exemple/capteur reçoit un payload JSON avec timestamp, clés 'temperature, hiumidite, pression', valeur float
- se connecte à la base de données robot1
- ajoute les valeurs recues dans la table mesures

## script python d'envoi de données par MQTT

- script générant des données cohérentes sur 24 heures pour disposer de données dans la base
