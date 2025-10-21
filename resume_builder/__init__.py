import os
import uuid
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, bcrypt, login_manager, migrate
from .models import (
    User,
    BasicInfo,
    Summary,
    Experience,
    Education,
    Skills,
    Language,
    BuiltResume,
    ResumeTheme,
    InviteCode,
)


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(project_root, ".env"))
from .config import config_by_env


def create_app():
    instance_path = os.path.join(project_root, "instance")
    app = Flask(
        __name__,
        instance_path=instance_path,
        template_folder="templates",
        static_folder="static",
    )
    flask_env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_env[flask_env])

    @app.context_processor
    def inject_feature_flags():
        return dict(features=app.config.get("FEATURE_FLAGS", {}))

    from .main import main_bp
    from .auth import auth_bp
    from .resume_builder_core import resume_bp
    from .admin import admin_bp
    from .job_application_tracker import job_app_tracker_bp

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            # First, try to convert the user_id to a UUID object.
            # This will catch any values that are not valid UUIDs.
            uuid.UUID(user_id)
        except ValueError:
            return None
        return User.query.get(user_id)

    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(resume_bp, url_prefix="/resume")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(job_app_tracker_bp, url_prefix="/application_tracker")

    @app.shell_context_processor
    def make_shell_context():
        """Returns a dictionary of variables to be made available in the shell."""
        return {
            "db": db,
            "User": User,
            "BasicInfo": BasicInfo,
            "Summary": Summary,
            "Experience": Experience,
            "Education": Education,
            "Skills": Skills,
            "Language": Language,
            "ResumeTheme": ResumeTheme,
            "BuiltResume": BuiltResume,
            "InviteCode": InviteCode,
        }

    return app
