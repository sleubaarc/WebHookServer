from flask import Blueprint, render_template_string
from app.models import WebhookEvent
import json
from collections import defaultdict
from datetime import datetime, timedelta

events_bp = Blueprint('events', __name__)

# Générer la liste des dates entre le 1er et le 15 septembre
start_date = datetime(2024, 9, 1)
end_date = datetime(2024, 9, 25)
date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

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

            if date in date_range:
                tickets_by_date[event_type][date] += 1

        except json.JSONDecodeError:
            grouped_events['Payload non valide'].append({'number': event.id})

    events_html = """
    <html>
        <head>
            <title>Événements Reçus</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                .ticket-card {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 10px 0;
                    background-color: #f9f9f9;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
            </style>
        </head>
        <body class="container mt-5">
            <h2 class="mb-4">Événements Reçus :</h2>
    """

    for event_type, tickets in grouped_events.items():
        ticket_counts = [tickets_by_date[event_type].get(date, 0) for date in date_range]
        chart_id = event_type.replace(' ', '_')

        events_html += f"""
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h4>{event_type}</h4>
            </div>
            <div class="card-body">
                <div class="row">
        """
        for ticket in tickets:
            events_html += f"""
            <div class="col-md-3">
                <div class="ticket-card">
                    <strong>Numéro de Ticket:</strong> {ticket.get('number', 'N/A')}<br>
                    <strong>Titre:</strong> {ticket.get('title', 'N/A')}<br>
                    <strong>Prix:</strong> {ticket.get('price', {}).get('amount', 'N/A')} {ticket.get('price', {}).get('currency', '')}<br>
                    <strong>Prénom du Participant:</strong> {ticket.get('buyer_first_name', 'N/A')}
                </div>
            </div>
            """
        events_html += f"""
                </div>
                <div class="p-3">
                    <canvas id="chart-{chart_id}"></canvas>
                </div>
            </div>
        </div>
        <script>
            new Chart(document.getElementById('chart-{chart_id}'), {{
                type: 'line',
                data: {{
                    labels: {date_range},
                    datasets: [{{
                        label: 'Nombre de tickets vendus par jour',
                        data: {ticket_counts},
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        fill: true,
                        pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                        pointRadius: 5,
                        tension: 0.3
                    }}]
                }},
                options: {{
                    scales: {{
                        x: {{
                            type: 'category',
                            min: '{date_range[0]}',
                            max: '{date_range[-1]}',
                            ticks: {{
                                autoSkip: false,
                                maxRotation: 45,
                                minRotation: 45
                            }}
                        }},
                        y: {{
                            beginAtZero: true,
                            max: 25  // ✅ Limite fixée à 50
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
