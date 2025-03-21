from flask import Flask
from application.database import db
import os
app=None




# Debugging Template Path

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///quiz.sqlite3"
    app.config["SECRET_KEY"] = "quiz_master_secure_key_2025"
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *
from application.models import User

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


if __name__=="__main__":
    app.run(debug=False)
    