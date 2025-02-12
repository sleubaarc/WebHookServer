from flask import Blueprint, render_template_string
from app.models import WebhookEvent
import json
from collections import defaultdict

events_bp = Blueprint('events', __name__)

@events_bp.route("/events")
def view_events():
    events = WebhookEvent.query.all()
    grouped_events = defaultdict(list)
    tickets_by_date = defaultdict(lambda: defaultdict(int))

    for event in events:
        try:
            payload = json.loads(event.payload)
            ticket = payload.get('details', {}).get('ticket', {})
            buyer = payload.get('details', {}).get('buyer', {})
            event_type = ticket.get('event', 'Inconnu')
            ticket['buyer_first_name'] = buyer.get('firstName', 'N/A')

            date = ticket.get('generatedAt', '')[:10]
            grouped_events[event_type].append(ticket)
            tickets_by_date[event_type][date] += 1

        except json.JSONDecodeError:
            grouped_events['Payload non valide'].append({'number': event.id})

    events_html = """
    <html>
        <head>
            <title>Événements Reçus</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body class="container mt-5">
            <h2 class="mb-4">Événements Reçus :</h2>
    """

    for event_type, tickets in grouped_events.items():
        dates = sorted(tickets_by_date[event_type].keys())
        ticket_counts = [tickets_by_date[event_type][date] for date in dates]

        chart_id = event_type.replace(' ', '_')

        events_html += f"""
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h4>{event_type}</h4>
            </div>
            <ul class="list-group list-group-flush">
        """
        for ticket in tickets:
            events_html += f"""
            <li class="list-group-item">
                <strong>Numéro de Ticket:</strong> {ticket.get('number', 'N/A')}<br>
                <strong>Titre:</strong> {ticket.get('title', 'N/A')}<br>
                <strong>Prix:</strong> {ticket.get('price', {}).get('amount', 'N/A')} {ticket.get('price', {}).get('currency', '')}<br>
                <strong>Prénom du Participant:</strong> {ticket.get('buyer_first_name', 'N/A')}
            </li>
            """
        events_html += f"""
            </ul>
            <div class="p-3">
                <canvas id="chart-{chart_id}"></canvas>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('chart-{chart_id}'), {{
                type: 'line',
                data: {{
                    labels: {dates},
                    datasets: [{{
                        label: 'Nombre de tickets vendus par jour',
                        data: {ticket_counts},
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        fill: true
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        </script>
        """

    events_html += """
            <div class="mt-4">
                <a href="/" class="btn btn-secondary">Retour à l'accueil</a>
            </div>
        </body>
    </html>
    """

    return render_template_string(events_html)
