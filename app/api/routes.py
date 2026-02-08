from flask import Blueprint, jsonify
from app.models import Contact

api_bp = Blueprint("api", __name__)

@api_bp.route("/contacts")
def api_contacts():
    contacts = Contact.query.all()
    return jsonify([
        {"name": c.name, "phone": c.phone, "email": c.email}
        for c in contacts
    ])
