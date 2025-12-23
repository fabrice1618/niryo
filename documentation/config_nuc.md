# Configuration NUC

## Adresse IP statique
```
network:
  version: 2
  ethernets:
    enp86s0:
      dhcp4: false
      addresses: [192.168.1.2/24]
      routes:
        - to: default
          via: 192.168.1.1
      nameservers:
        addresses: [192.168.1.1]
```

```
sudo netplan generate && sudo netplan apply
```

## Création utilisateur

```
sudo useradd -m -s /bin/bash fab 
sudo usermod -aG sudo fab
sudo passwd fab 
# ghjk
$ id
uid=1001(fab) gid=1001(fab) groupes=1001(fab),27(sudo)
```

## création base de données


```
$ cd database
$ mysql -u dba -p

mysql> source creation.sql

```

