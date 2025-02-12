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
- MySQL / MariaDB
- Docker & Docker Compose (optionnel)

### **Cloner le projet**
git clone https://github.com/votre-utilisateur/webhook-server.git
cd webhook-server

### ** Création de l'environnement virtuel **
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt

### *** Configurer les variables d'environnement ***
DB_USER=root
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=3306
DB_NAME=webhook
SECRET_KEY=AEeyJhbGciOiJIUzUxMiIsImlzcyI6
