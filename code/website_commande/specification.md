# Site web - envoi de commandes au robot

## fonctions

- page HTML permettant l'envoi de commandes sur l'API du robot (mock ou réel)
- boutons pour envoyer `POST /color` avec `{"color": "red"}`, `{"color": "green"}`, `{"color": "blue"}`
- affichage du retour de l'API (succès/erreur)
- site python flask

## API cible

Le mock robot (`code/mock_robot/app.py`) expose :
- `POST /color` — body JSON `{"color": "red|green|blue"}` — réponse `{"status": "ok", "color": "..."}` ou `{"error": "..."}`
- Port par défaut : 3000
