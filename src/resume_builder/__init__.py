import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///resume_builder.db")
    from .routes import main_bp
    from .auth import auth_bp
    db = SQLAlchemy()
    db.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
