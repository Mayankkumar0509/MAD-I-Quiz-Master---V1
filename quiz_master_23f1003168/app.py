from flask import Flask
from application.database import db
import os

app = None

def create_app():
    app = Flask(__name__)

    # Disable debug mode for production
    app.debug = False

    # Database configuration (SQLite file inside project)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "quiz_master_secure_key_2025"

    # Initialize DB
    db.init_app(app)
    app.app_context().push()

    return app

app = create_app()

# Import controllers after app is created
from application.controllers import *
from application.models import User

# Create default admin user if not exists
with app.app_context():
    admin_user = User.query.filter_by(type="admin").first()
    if not admin_user:
        admin = User(
            username="admin@main.com",
            password="1234",
            fullname="Mayank kumar",
            qualification="BSc in data science",
            dob="2000-01-01",
            type="admin"
        )
        db.session.add(admin)
        db.session.commit()


# HF Spaces requires this
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))  # HF PORT
    app.run(host="0.0.0.0", port=port)

    
