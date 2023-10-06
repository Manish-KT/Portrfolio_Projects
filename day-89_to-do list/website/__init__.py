from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .model import Users, Task, Subtask

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Ensure that the database is created if it doesn't exist
    with app.app_context():
        if not path.exists("website/" + DB_NAME):
            db.create_all()
            print("Created Database!")

    # flask_login initialization

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to access this page."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app
