# Webhook Server - Petzi

Ce projet est un serveur Flask qui gère des webhooks pour les événements de billetterie Petzi.  
Il reçoit des webhooks, stocke les données en base de données MySQL et affiche les tickets achetés sous forme de page web interactive avec des graphiques.

---

## Fonctionnalités

- Réception de webhooks via une API sécurisée
- Vérification de la signature HMAC des webhooks
- Stockage des événements dans une base de données MySQL
- Affichage des tickets achetés regroupés par événement
- Graphiques interactifs des ventes par jour
- Déploiement avec **Docker** et **Nginx** en reverse proxy

---

## Installation et Configuration

### **Prérequis**
- Python 3.x
- MySQL / MariaDB, installation possible depuis : https://dev.mysql.com/downloads/mysql/
- Docker & Docker Compose (optionnel)

### **Cloner le projet**
git clone https://github.com/sleubaarc/WebHookServer.git

### **Création de l'environnement virtuel**
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt

### **Création de la DB**
Il est important de créer un user et un password avec l'installation de mysql en local avant d'effectuer la configuration en local de la DB.
![alt text](image.png)

un script de création de DB "createdatabase.py est à disposition à la source du projet une fois la db créée.
- python.exe createdatabase.py

### **Création de l'environnement virtuel**
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt

### **Configurer les variables d'environnement (fichier.env)**
- DB_USER=root
- DB_PASSWORD=à choix
- DB_HOST=localhost
- DB_PORT=3306
- DB_NAME=webhook
- SECRET_KEY=AEeyJhbGciOiJIUzUxMiIsImlzcyI6