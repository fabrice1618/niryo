Sources : ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html))

---

# 🧩 1. Connexion, Calibration et Gestion du Robot

## **Fonctions principales**
- `connect(ip_address)`  
- `close_connection()`  
- `calibrate(mode)`  
- `calibrate_auto()`  

## **Description**  
Ce groupe rassemble toutes les fonctions permettant d’établir, maintenir et réinitialiser la connexion TCP entre un script Python et un robot Niryo.  
`connect()` ouvre la communication avec l’adresse IP spécifiée, tandis que `close_connection()` ferme proprement la session. La calibration (`calibrate()` ou `calibrate_auto()`) permet d’assurer que les moteurs du bras sont correctement référencés avant l’exécution de mouvements. Le mode peut être manuel ou automatique. Cette étape est indispensable : sans calibration, les mouvements peuvent être inexacts ou refusés.  
Au final, ce thème couvre les opérations d’initialisation obligatoires avant tout usage avancé du robot. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0/api/api.html?utm_source=openai))

---

# 🦾 2. Outils, TCP, Préhension et Effector Management

## **Fonctions principales**
- `enable_tcp(enable)`  
- `set_tcp(...)`  
- `reset_tcp()`  
- `tool_reboot()`  
- `activate_electromagnet(pin)` / `deactivate_electromagnet(pin)`  

## **Description**  
Ces fonctions gèrent l’“effector” du robot : outils, électroaimants, ventouses et paramètres géométriques du point outil (TCP).  
La fonction `enable_tcp()` active/désactive l’utilisation d’un TCP personnalisé, et `set_tcp()` permet de définir une transformation entre l’outil physique et son origine logique. Cela améliore la précision lors de manipulations complexes.  
`tool_reboot()` force un redémarrage du moteur d’outil pour corriger des erreurs d’overload.  
Enfin, les fonctions d’activation d’électroaimant permettent de saisir/lâcher des objets sans gripper mécanique.  
Ce thème est essentiel pour toutes les tâches de manipulation et d’assemblage. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html?utm_source=openai))

---

# 📍 3. Poses, Coordonnées et Objets de Position

## **Classes et fonctions principales**
- `PoseObject`  
- `PoseMetadata`  
- `PoseObject.copy_with_offsets()`  
- `PoseObject.quaternion()`  
- `JointsPosition`  

## **Description**  
Ce thème regroupe les classes qui encapsulent la représentation spatiale d’un objet ou de l’outil du robot.  
`PoseObject` stocke une pose complète : position (x, y, z), angles (roll, pitch, yaw) et métadonnées (frame, unité, version TCP). La classe permet aussi de convertir vers quaternion ou d’appliquer des offsets.  
`JointsPosition` représente une position robot par valeurs articulaires, pratique pour mouvements en configuration.  
Ces objets sont fondamentaux pour composer, transformer et transmettre des instructions de mouvement cohérentes et répétables. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html?utm_source=openai))

---

# 🗺️ 4. Workspaces et Frames Dynamiques

## **Fonctions principales**
- `save_workspace_from_robot_poses(...)`  
- `save_workspace_from_points(...)`  
- `delete_workspace(name)`  
- `get_workspace_list()`  
- `get_workspace_ratio(name)`  
- `get_saved_dynamic_frame_list()`  
- `edit_dynamic_frame()`  
- `delete_dynamic_frame()`  

## **Description**  
Les “workspaces” sont des zones calibrées où le robot effectue des tâches (pick-and-place, scan, etc.).  
Les fonctions permettent soit d’enregistrer un workspace depuis quatre poses du robot (`save_workspace_from_robot_poses()`), soit depuis quatre points définis comme coordonnées 3D (`save_workspace_from_points()`).  
La gestion inclut la suppression, l’obtention de la liste des espaces enregistrés et la récupération de leurs paramètres.  
Les “dynamic frames” sont des repères utilisateurs personnalisés. Ils permettent d’exprimer des poses par rapport à des objets mobiles ou repositionnés.  
Ce thème structure toute la spatialisation avancée des tâches. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html?utm_source=openai))

---

# 🌈 5. LED Ring & Signalisations Lumineuses

## **Fonctions principales**
- `led_ring_rainbow()`  
- `led_ring_rainbow_cycle()`  
- `led_ring_rainbow_chase()`  
- `led_ring_go_up()` / `go_up_down()`  
- `led_ring_snake()`  
- `led_ring_breath()`  
- `led_ring_custom(colors)`  
- `led_ring_flashing()`  
- `led_ring_wipe()`  
- `led_ring_alternate()`  

## **Description**  
Ce groupe couvre toutes les animations du cercle de LEDs, très utile pour le feedback utilisateur (état, progression, erreurs).  
Chaque fonction génère un motif visuel différent : cycles arc‑en‑ciel, respiration, clignotement, “snake”, balayage, alternance de couleurs ou dessin complet personnalisé avec 30 LEDs.  
La plupart acceptent :  
- `period` : durée d’une animation,  
- `iterations` : répétitions,  
- `wait` : attendre ou non la fin de l’animation.  
Ces outils permettent une communication non verbale riche entre robot et opérateur. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html?utm_source=openai))

---

# 🔧 6. Exceptions, États matériels et Énumérations

## **Éléments principaux**
- Exceptions : `NiryoRobotException`, `TcpCommandException`, etc.  
- Énumérations : `CalibrateMode`, `ConveyorID`, `ToolID`, `Axis`, etc.  
- Objets matériels : `HardwareStatusObject`, `DigitalPinObject`, `AnalogPinObject`  

## **Description**  
Ce thème regroupe tous les mécanismes de contrôle d’erreur et de description “bas niveau” du matériel.  
Les exceptions permettent d’interpréter les erreurs réseau, TCP, réponses invalides ou matériel absent.  
Les énumérations définissent des identifiants constants pour outils, convoyeurs, axes, etc., garantissant des scripts moins ambigus et plus lisibles.  
Les objets matériels fournissent une vision précise de l’état du robot : température, tensions moteurs, erreurs, état des pins.  
Ce thème est indispensable pour la robustesse et le diagnostic des applications. ([niryorobotics.github.io](https://niryorobotics.github.io/pyniryo/v1.2.0-1/api/api.html?utm_source=openai))
