# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a teaching project for B3 industrial automation students at the Technique & Nucléaire department, demonstrating client-server infrastructure for Niryo robot control. The system integrates:
- Niryo robot control via Python SDK
- MQTT message broker (Mosquitto) for sensor data
- MySQL database for telemetry storage
- Flask web interfaces for robot command and control
- Supervision/monitoring dashboards (Node-RED/Grafana)

## Architecture

### Three-tier System

1. **Robot Layer**: Niryo robotic arm controlled via Python SDK (or mock)
   - Mock robot (`code/mock_robot/`): Flask API on port 3000, simulates LED blink
   - Endpoint: `POST /color` with JSON body `{"color": "red|green|blue"}`
   - Publishes events to MQTT topic `robot3/events` after each action
   - Real robot: TCP connection via pyniryo SDK, calibration required before movement

2. **Middleware Layer**:
   - MQTT broker (Mosquitto) on port 1883 with authentication
   - `event_handler.py`: subscribes to `robot3/events` topic
   - Receives JSON payloads: `{"event": "...", "timestamp": epoch, "data": {...}}`
   - Writes events to MySQL `events` table

3. **Database Layer**: MySQL with multi-robot support
   - 4 databases: `robot1`, `robot2`, `robot3`, `robot4`
   - Each robot has dedicated user (e.g., `robot1`/`robot1pass`)
   - `grafana_reader` user with SELECT on all robot databases
   - Table `events(event_id, timestamp, event_type, color, status, raw_json)` for robot events

### Code Organization

```
code/
├── diag_api/             # Interactive API diagnostic tool
│   ├── diag_api.py       # POST /color test tool with color menu
│   └── README.md
├── diag_mqtt/            # Interactive MQTT diagnostic tool
│   └── diag_mqtt.py      # Subscribe/Publish test tool
├── diag_sql/             # Interactive SQL diagnostic tool
│   ├── diag_sql.py       # MySQL query tool with predefined + free queries
│   └── README.md
├── mock_robot/           # Flask API mock simulating the Niryo robot (port 3000)
│   ├── app.py            # POST /color endpoint + MQTT event publishing
│   ├── requirements.txt
│   └── README.md
├── mqtt_message/         # MQTT subscriber → MySQL event writer
│   ├── event_handler.py  # Subscribes to robot3/events, inserts into events table
│   └── requirements.txt
├── website_commande/     # Flask web interface for robot commands (TODO)
│   └── specification.md  # Spec only, no code yet
└── website_pilotage/     # Flask web interface for robot piloting (port 5000)
    ├── app.py            # Proxy vers API robot + sert le template HTML
    ├── templates/
    │   └── index.html    # Page Bootstrap avec boutons couleur
    ├── requirements.txt
    └── README.md

database/
├── creation.sql          # Database + users setup (4 robots, grafana_reader, mesures table)
└── creation_events.sql   # Events table creation (for robot3)

documentation/
├── programme_Niryo.md    # Course syllabus and pedagogical objectives
├── sdk.md                # Niryo SDK reference documentation
├── config_nuc.md         # NUC server configuration
├── config_routeur.md     # Router configuration
├── install_package_python.md
├── reseau.md / reseau2.md
├── Niryo-reseau.drawio.png
└── Niryo-Synoptique.drawio.png
```

## Common Commands

### Database Setup

Initialize MySQL databases and users:
```bash
cd database
mysql -u dba -p
source creation.sql
```

## Development Guidelines

### Niryo Robot SDK

- **Always calibrate** before movement: `calibrate_auto()` or `calibrate(mode)`
- Connection sequence: `connect(ip_address)` → calibrate → operations → `close_connection()`
- Use `PoseObject` for spatial positioning (x, y, z, roll, pitch, yaw)
- TCP (Tool Center Point) must be configured for precision tasks
- LED ring functions available for visual feedback

### MQTT Event Format

Robot events published/consumed on topic `robot3/events`:
```json
{"event": "color_done", "timestamp": 1709136000.0, "data": {"color": "red", "status": "success"}}
{"event": "color_error", "timestamp": 1709136000.0, "data": {"color": "yellow"}}
```

### Database Schema

**`events` table** (robot3, robot events from MQTT):
- `event_type`: e.g., "color_done", "color_error"
- `color`, `status`: extracted from event data
- `raw_json`: full MQTT message preserved
- Indexed on `timestamp`, `event_type`, and composite

### Flask API Endpoints

Mock robot (code/mock_robot):
- `POST /color` with body `{"color": "red|green|blue"}` — simulate LED blink + publish MQTT event

Website commande (code/website_commande — not yet implemented):
- Web UI to send commands to the robot API

### Network Configuration

NUC server static IP (netplan):
```yaml
enp86s0:
  dhcp4: false
  addresses: [192.168.1.2/24]
  routes:
    - to: default
      via: 192.168.1.1
```

## Project Context

This is an educational project for a 21-hour course module covering:
- Session 1: Robot networking and SDK basics
- Session 2: Python movement programming
- Session 3: External sensors and I/O
- Session 4: Flask API for remote control
- Session 5: Node-RED/Grafana supervision
- Session 6: Final integrated project demonstration

The goal is to create a minimal industrial workstation: sensor → decision → robot movement → monitoring.
