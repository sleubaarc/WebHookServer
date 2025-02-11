from flask import Blueprint, request, jsonify
from app import db
from app.models import WebhookEvent
import hmac
import hashlib
import json

webhook_bp = Blueprint('webhook', __name__)
SECRET = "AEeyJhbGciOiJIUzUxMiIsImlzcyI6"  # Remplacer par votre secret webhook

def verify_signature(request_body: bytes, signature_header: str) -> bool:
    try:
        signature_parts = dict(part.split("=") for part in signature_header.split(","))
        body_to_sign = f'{signature_parts["t"]}.{request_body.decode()}'.encode()
        expected_signature = hmac.new(SECRET.encode(), body_to_sign, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, signature_parts["v1"])
    except Exception:
        return False

@webhook_bp.route("/webhook", methods=["POST"])
def receive_webhook():
    signature = request.headers.get("Petzi-Signature")
    if not signature:
        return jsonify({"error": "Missing signature"}), 400

    body = request.data

    if not verify_signature(body, signature):
        return jsonify({"error": "Invalid signature"}), 403

    event = WebhookEvent(payload=body.decode())
    db.session.add(event)
    db.session.commit()

    return jsonify({"status": "success"})
