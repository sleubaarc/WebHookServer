from flask import Blueprint

# Import des blueprints
from app.routes.home import home_bp
from app.routes.events import events_bp
from app.routes.webhook import webhook_bp

# Liste des blueprints à enregistrer
blueprints = [home_bp, events_bp, webhook_bp]