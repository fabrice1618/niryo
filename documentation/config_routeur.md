# Configuration routeur

## Accès avec application **tether**

Mot de passe: irup/42

Mode routeur:
interface WAN: IP dynamique

### Réseau 2.4 GHz
SSID: Niryo

password: IRUP-42/Niryo

### Réseau 5 GHz
SSID: Niryo_5G

password: IRUP-42/Niryo

## Adressage:

| Adresses | |
|----------|-|
| 192.168.0.1  | Gateway |
| 192.168.0.2  | Serveur |
| 192.168.0.11  | Robot 1 |
| 192.168.0.12  | Robot 2 |
| 192.168.0.13  | Robot 3 |
| 192.168.0.14  | Robot 4 |
| 192.168.0.15  | Robot 5 |
| 192.168.0.20  | début DHCP |
| 192.168.0.253  | fin DHCP |
| 192.168.0.255  | broadcast |

## scan du réseau du robot

nmap -sn 192.168.0.0/24