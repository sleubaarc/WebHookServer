from flask import Blueprint, render_template_string

home_bp = Blueprint('home', __name__)

@home_bp.route("/")
def home():
    html_content = """
    <html>
        <head>
            <title>Petzi Webhook Server</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="container mt-5">
            <div class="text-center">
                <h1 class="mb-4">Bienvenue sur le Serveur Webhook de Petzi</h1>
                <p>Le serveur est en cours d'exécution et prêt à recevoir des webhooks.</p>
                <a href="/events" class="btn btn-primary">Voir les événements</a>
            </div>
        </body>
    </html>
    """
    return render_template_string(html_content)
