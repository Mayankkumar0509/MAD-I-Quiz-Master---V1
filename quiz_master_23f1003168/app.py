from flask import Flask
from application.database import db
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///quiz.sqlite3").replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "mk0509")

    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create tables
        
        # Import models after db initialization
        from application.models import User
        
        # Create admin user if doesn't exist
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

    return app

app = create_app()

# Import controllers after app creation
from application.controllers import *

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
