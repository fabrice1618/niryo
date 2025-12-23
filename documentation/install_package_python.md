# Installations sur robot

## Installation offline via un fichier .whl (recommandé)
Étape 1 — Télécharger le package sur un PC ayant Internet

Sur ton PC :
```
pip3 download paho-mqtt
```
Cela crée un fichier du type : paho_mqtt‑1.6.1‑py3-none-any.whl

Étape 2 — Copier le fichier sur le robot

Utilise un câble Ethernet ou un clé USB :

    via scp :
```
scp paho_mqtt-*.whl niryo@192.168.0.26:/home/niryo/
```
    ou copie depuis une clé USB après t’être connecté en SSH sur le robot.

Étape 3 — Installer offline sur le robot

Une fois connecté en SSH :
```
pip3 install /home/niryo/paho_mqtt-*.whl
```

## Connnexion SSH

login: niryo

password: robotics

test script 4:
mosquitto_sub -h 192.168.0.92 -p 1883 -u mqtt -P mqtt -t hello

test script5:
mosquitto_pub -h 192.168.0.92 -u mqtt -P mqtt -t hello -m red
$ mosquitto_pub -h 192.168.0.92 -u mqtt -P mqtt -t hello -m green
$ mosquitto_pub -h 192.168.0.92 -u mqtt -P mqtt -t hello -m blue


## installation flask

mkdir flask_arm
pip3 download flask -d flask_arm --no-binary :all:
scp -r flask_arm niryo@192.168.0.26:/home/niryo/
pip3 install --no-index --find-links . flask


$ curl -X POST http://192.168.0.26:3000/color -H "Content-Type: application/json" -d '{"color":"red"}'
{"color":"red","status":"ok"}
$ curl -X POST http://192.168.0.26:3000/color -H "Content-Type: application/json" -d '{"color":"blue"}'
{"color":"blue","status":"ok"}
$ curl -X POST http://192.168.0.26:3000/color -H "Content-Type: application/json" -d '{"color":"green"}'
{"color":"green","status":"ok"}
