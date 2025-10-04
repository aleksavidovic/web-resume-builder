import uuid
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, ForeignKey, TypeDecorator, CHAR
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
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
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
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class EntryTitleMixin:
    entry_title = db.Column(db.String(255), nullable=False)

# Association Tables
built_resume_experience = Table(
    "built_resume_experience",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id"), primary_key=True),
    Column("experience_id", GUID(), ForeignKey("experience.id"), primary_key=True),
)

built_resume_education = Table(
    "built_resume_education",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id"), primary_key=True),
    Column("education_id", GUID(), ForeignKey("education.id"), primary_key=True),
)

built_resume_skills = Table(
    "built_resume_skills",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id"), primary_key=True),
    Column("skills_id", GUID(), ForeignKey("skills.id"), primary_key=True),
)

built_resume_language = Table(
    "built_resume_language",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id"), primary_key=True),
    Column("language_id", GUID(), ForeignKey("language.id"), primary_key=True),
)

class User(db.Model, UserMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(70), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    basic_infos = db.relationship(
        "BasicInfo", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    summaries = db.relationship(
        "Summary", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    experiences = db.relationship(
        "Experience", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    education = db.relationship(
        "Education", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    skills = db.relationship(
        "Skills", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    languages = db.relationship(
        "Language", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )
    resumes = db.relationship(
        "BuiltResume", backref="user", lazy="selectin", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"


class BasicInfo(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)
    contact_phone = db.Column(db.String(50), nullable=False)
    linkedin_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_entry_title_uc"),
    )


class Summary(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=True, default="")

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_summary_title_uc"),
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
        db.UniqueConstraint("user_id", "entry_title", name="_user_experience_title_uc"),
    )


class Education(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    degree_name = db.Column(db.String(255), nullable=False)
    school_name = db.Column(db.String(255), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    date_finished = db.Column(db.Date, nullable=True)

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_education_title_uc"),
    )


class Skills(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    skill_group_title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_skills_title_uc"),
    )


class Language(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(128), nullable=False)
    proficiency = db.Column(db.String(128), nullable=False)

    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_language_title_uc"),
    )

class ResumeTheme(db.Model, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    styles = db.Column(db.Text, nullable=False)


class BuiltResume(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)

    basic_info_id = db.Column(GUID(), db.ForeignKey("basic_info.id"), nullable=False) 
    summary_id = db.Column(GUID(), db.ForeignKey("summary.id"), nullable=False)
    theme_id = db.Column(GUID(), db.ForeignKey("resume_theme.id"), nullable=False)

    basic_info = relationship("BasicInfo")
    summary = relationship("Summary")
    theme = relationship("ResumeTheme")

    experience = relationship(
        "Experience", secondary=built_resume_experience, backref="built_resumes"
    )
    education = relationship(
        "Education", secondary=built_resume_education, backref="built_resumes"
    )
    skills = relationship(
        "Skills", secondary=built_resume_skills, backref="built_resume"
    )
    languages = relationship(
        "Language", secondary=built_resume_language, backref="built_resume"
    )


    user_id = db.Column(GUID(), db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_built_resumes_title_uc"),
    )

