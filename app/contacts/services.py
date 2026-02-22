import re
from app.models import Contact
from app.extensions import db
from app.exceptions import ContactExistsError, InvalidPhoneError

PHONE_PATTERN = re.compile(r"^\d{10}$")

def _validate_phone(phone):
    """Allow only 10-digit numbers."""
    phone = (phone or "").strip()
    if not phone or not PHONE_PATTERN.match(phone):
        raise InvalidPhoneError("Phone must be exactly 10 digits")
    return phone

def add_contact(data):
    name = (data.get("name") or "").strip()
    phone = _validate_phone(data.get("phone"))
    if not name:
        return

    if Contact.query.filter_by(phone=phone).first():
        raise ContactExistsError("Contact already exists")

    contact = Contact(
        name=name,
        phone=phone,
        email=(data.get("email") or "").strip() or None
    )
    db.session.add(contact)
    db.session.commit()

def get_contact(contact_id):
    return Contact.query.get(contact_id)

def update_contact(contact_id, data):
    contact = Contact.query.get(contact_id)
    if not contact:
        return
    name = (data.get("name") or "").strip()
    phone = _validate_phone(data.get("phone"))
    if not name:
        return
    existing = Contact.query.filter(Contact.phone == phone, Contact.id != contact_id).first()
    if existing:
        raise ContactExistsError("Another contact already has this phone")
    contact.name = name
    contact.phone = phone
    contact.email = (data.get("email") or "").strip() or None
    db.session.commit()

def list_contacts(search=None, page=1, per_page=10, favorites_only=False):
    q = Contact.query
    if search and search.strip():
        term = f"%{search.strip()}%"
        q = q.filter(Contact.name.ilike(term))
    if favorites_only:
        q = q.filter(Contact.is_favorite == True)
    q = q.order_by(Contact.is_favorite.desc(), Contact.created_at.desc())
    pagination = q.paginate(page=page, per_page=per_page)
    return pagination

def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)
    if contact:
        db.session.delete(contact)
        db.session.commit()

def toggle_favorite(contact_id):
    contact = Contact.query.get(contact_id)
    if contact:
        contact.is_favorite = not contact.is_favorite
        db.session.commit()
        return contact.is_favorite
    return None
