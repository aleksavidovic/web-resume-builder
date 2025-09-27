import uuid
from datetime import datetime, timezone 
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses PosgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int


    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class TimeStampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class EntryTitleMixin:
    entry_title = db.Column(db.String(50), nullable=False)


class User(db.Model, UserMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    basic_infos = db.relationship("BasicInfo", backref="user", lazy=True, cascade="all, delete-orphan")
    summaries = db.relationship("Summary", backref="user", lazy=True, cascade="all, delete-orphan")
    experiences = db.relationship("Experience", backref="user", lazy=True, cascade="all, delete-orphan")
    # TODO: Educations, Skills, Languages

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"


class BasicInfo(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contact_email = db.Column(db.String(30), nullable=False)
    contact_phone = db.Column(db.String(30), nullable=False)
    linkedin_url = db.Column(db.String(100), nullable=True)
    github_url = db.Column(db.String(100), nullable=True)

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'entry_title', name='_user_entry_title_uc'),
    )


class Summary(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=True, default="")

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'entry_title', name='_user_summary_title_uc'),
    )

class Experience(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    job_title = db.Column(db.String(50), nullable=False, default="")
    company_name = db.Column(db.String(50), nullable=False, default="")
    date_started = db.Column(db.Date, nullable=False)
    date_finished = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True, default="")

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'entry_title', name='_user_experience_title_uc'),
    )
