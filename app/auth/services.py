from app.extensions import db, bcrypt
from app.models import User

def create_user(data):
    hashed = bcrypt.generate_password_hash(data["password"]).decode()
    user = User(email=data["email"], password=hashed)
    db.session.add(user)
    db.session.commit()

def authenticate_user(data):
    user = User.query.filter_by(email=data["email"]).first()
    if user and bcrypt.check_password_hash(user.password, data["password"]):
        return user
    return None
