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

1. **Robot Layer**: Niryo robotic arm controlled via Python SDK
   - Endpoints: `/color/red`, `/color/blue`, `/color/green`, `/autocalibrate`
   - TCP connection to robot IP address
   - Calibration required before movement operations

2. **Middleware Layer**:
   - MQTT broker (Mosquitto) on port 1883 with authentication
   - Python MQTT subscriber listening on `exemple/capteur` topic
   - Receives JSON payloads: `{timestamp, temperature, humidite, pression}`
   - Writes measurements to MySQL database

3. **Database Layer**: MySQL with multi-robot support
   - 4 databases: `robot1`, `robot2`, `robot3`, `robot4`
   - Each robot has dedicated user (e.g., `robot1`/`robot1pass`)
   - `grafana_reader` user with SELECT on all robot databases
   - Table structure: `mesures(mesure_id, timestamp, cle, valeur)`

### Code Organization

```
code/
├── api_robot_test/       # Flask API mock for robot endpoints (testing)
├── mqtt_message/         # MQTT subscriber + database writer
└── website_commande/     # Flask web interface for robot commands

database/
└── creation.sql          # Database setup script

documentation/
├── programme_Niryo.md    # Course syllabus and pedagogical objectives
├── sdk.md                # Niryo SDK reference documentation
└── config_nuc.md         # NUC server configuration
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

### MQTT Message Format

Expected JSON structure for sensor data:
```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "temperature": 23.5,
  "humidite": 65.2,
  "pression": 1013.25
}
```

Topic: `exemple/capteur`

### Database Schema

The `mesures` table uses a flexible key-value structure:
- `cle`: measurement type (e.g., "temperature", "humidite", "pression")
- `valeur`: float measurement value
- Indexed on `timestamp`, `cle`, and composite `(timestamp, cle)`

### Flask API Endpoints

Robot control endpoints (to implement or test):
- `POST /color/red` - Execute red object sequence
- `POST /color/blue` - Execute blue object sequence
- `POST /color/green` - Execute green object sequence
- `POST /autocalibrate` - Trigger automatic calibration

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
