from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .auth.routes import auth_bp
from .contacts.routes import contacts_bp
from .api.routes import api_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        # Add is_favorite column if missing (existing databases)
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("ALTER TABLE contact ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
                conn.commit()
        except Exception:
            pass

    return app
