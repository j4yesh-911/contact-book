from app.models import Contact
from app.extensions import db
from app.exceptions import ContactExistsError

def add_contact(data):
    if Contact.query.filter_by(phone=data["phone"]).first():
        raise ContactExistsError("Contact already exists")

    contact = Contact(
        name=data["name"],
        phone=data["phone"],
        email=data["email"]
    )
    db.session.add(contact)
    db.session.commit()

def list_contacts():
    return Contact.query.order_by(Contact.created_at.desc()).all()

def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    db.session.delete(contact)
    db.session.commit()
