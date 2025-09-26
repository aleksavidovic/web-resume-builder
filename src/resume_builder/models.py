from datetime import datetime, timezone 
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    posts = db.relationship("BasicInfo", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"


class BasicInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=True, default="")
    job_title = db.Column(db.String(50), nullable=True, default="")
    address = db.Column(db.String(50), nullable=True, default="")
    contact_email = db.Column(db.String(30), nullable=True, default="")
    contact_phone = db.Column(db.String(30), nullable=True, default="")
    linkedin_url = db.Column(db.String(100), nullable=True, default="")
    github_url = db.Column(db.String(100), nullable=True, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    summary_name = db.Column(db.String(50), nullable=False, default="")
    summary_content = db.Column(db.Text, nullable=True, default="")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
