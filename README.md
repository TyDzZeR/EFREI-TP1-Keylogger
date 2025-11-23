# EFREI-TP1-Keylogger
Rendu du TP : LAB 1 – Extension Avancée : Projet de Simulation Keylogger par Steve NGUYEN et Djaganadane MOUROUGAYANE - ING3-APP-RS1

## Description du Projet

Ce projet est une simulation technique d'une architecture de **Command & Control (C2)**. L'objectif est de démontrer le fonctionnement d'un Keylogger piloté à distance par un serveur attaquant.

Le système respecte l'architecture demandée dans le sujet "Lab 1 Extended" et se compose de trois éléments :
1.  **La Victime (Client)** : Un script Python furtif qui capture les frappes et exécute des ordres.
2.  **L'Attaquant (Serveur C2)** : Une API Flask qui centralise les données exfiltrées.
3.  **Le Dashboard (Contrôleur)** : Une interface graphique Web pour surveiller et piloter les victimes en temps réel.

## Architecture Technique

* **Réseau :** Communication isolée via VirtualBox Internal Network (`intnet`).
* **Protocole Principal :** HTTP (REST API via POST).
* **Protocole Secondaire :** TCP Raw Sockets (pour l'exfiltration discrète).
* **Format des données :** JSON (`UUID`, `Keys`, `Timestamp`).

## Fonctionnalités Implémentées

### Côté Victime (Malware)
* **Capture temps réel :** Interception des événements clavier via la librairie `pynput`.
* **Identification Unique :** Génération d'un UUID aléatoire au démarrage pour identifier la session.
* **Exfiltration Hybride :** Capacité de basculer dynamiquement entre HTTP (port 5000) et TCP (port 9000).
* **Heartbeat & Résilience :** Envoi périodique de requêtes pour recevoir des ordres même sans activité clavier.
* **Exécution d'ordres distants :** Gestion des commandes `start`, `stop`, `flush`, `switch_mode`.

### Côté Attaquant (Serveur & Dashboard)
* **Serveur Web Flask :** Réception et stockage des logs dans des fichiers structurés (`/victims_data`).
* **Serveur TCP :** Script dédié à la réception des données brutes (Socket).
* **Interface Graphique (GUI) :** Dashboard style "Dark Mode".
    * Liste automatique des victimes actives.
    * Affichage des logs en streaming (Auto-refresh).
    * Panneau de contrôle complet (Boutons d'action).

## Structure du Projet

```text
Lab1-Keylogger/
│
├── Attacker/                   # Code pour la VM Attaquant (192.168.10.10)
│   ├── server.py               # Serveur C2 Principal (Flask + GUI)
│   ├── tcp_server.py           # Récepteur TCP (Port 9000)
│   ├── victims_data/           # Stockage des logs (généré automatiquement)
│   └── templates/
│       └── dashboard.html      # Interface Web (HTML/JS/CSS)
│
├── Victim/                     # Code pour la VM Victime (192.168.10.20)
│   └── client.py               # Le Malware (Keylogger)
│
├── requirements.txt            # Liste des dépendances
└── README.md                   # Documentation
