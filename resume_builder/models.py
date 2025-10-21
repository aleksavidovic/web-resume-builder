import uuid
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Table, Column, ForeignKey, TypeDecorator, CHAR, select, func
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
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id", ondelete="CASCADE"), primary_key=True),
    Column("experience_id", GUID(), ForeignKey("experience.id", ondelete="CASCADE"), primary_key=True),
)

built_resume_education = Table(
    "built_resume_education",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id", ondelete="CASCADE"), primary_key=True),
    Column("education_id", GUID(), ForeignKey("education.id", ondelete="CASCADE"), primary_key=True),
)

built_resume_skills = Table(
    "built_resume_skills",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id", ondelete="CASCADE"), primary_key=True),
    Column("skills_id", GUID(), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

built_resume_language = Table(
    "built_resume_language",
    db.Model.metadata,
    Column("built_resume_id", GUID(), ForeignKey("built_resume.id", ondelete="CASCADE"), primary_key=True),
    Column("language_id", GUID(), ForeignKey("language.id", ondelete="CASCADE"), primary_key=True),
)


class InviteCode(db.Model, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    redeemed = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(
        GUID(),
        db.ForeignKey("user.id", ondelete="SET NULL"),
        # unique=True,  <-- REMOVED
        nullable=True
    )
    user = db.relationship("User", back_populates="redeemed_code")

    __table_args__ = (
        db.UniqueConstraint('user_id', name='_invitecode_user_id_uc'),
    )

    def __repr__(self):
        return f"InviteCode:\nCode: '{self.code}'\nDesc: '{self.description}'\nReedemed: {'Yes' if self.redeemed else 'No'}\nUser: {self.user}"


class User(db.Model, UserMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(70), nullable=False) # <-- REMOVED unique=True
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    basic_infos = db.relationship(
        "BasicInfo",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    summaries = db.relationship(
        "Summary",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    experiences = db.relationship(
        "Experience",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    education = db.relationship(
        "Education",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    skills = db.relationship(
        "Skills",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    languages = db.relationship(
        "Language",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    resumes = db.relationship(
        "BuiltResume",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    redeemed_code = db.relationship("InviteCode", back_populates="user", uselist=False)

    job_applications = db.relationship(
        "JobApplication",
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        db.UniqueConstraint('username', name='_user_username_uc'),
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_active_count(cls):
        """Returns the count of active users"""
        count_stmt = select(func.count(cls.id)).where(cls.is_active == True)
        return db.session.scalar(count_stmt)

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

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="basic_infos")

    built_resumes = db.relationship("BuiltResume", back_populates="basic_info")

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_entry_title_uc"),
    )


class Summary(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=True, default="")

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="summaries")

    built_resumes = db.relationship("BuiltResume", back_populates="summary")

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

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="experiences")

    built_resumes = db.relationship(
        "BuiltResume",
        secondary=built_resume_experience,
        back_populates="experience"
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_experience_title_uc"),
    )

    def __repr__(self):
        return f"Experience('{self.company_name} | {self.date_started} | {self.date_finished}')"


class Education(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    degree_name = db.Column(db.String(255), nullable=False)
    school_name = db.Column(db.String(255), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    date_finished = db.Column(db.Date, nullable=True)

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="education")

    built_resumes = db.relationship(
        "BuiltResume",
        secondary=built_resume_education,
        back_populates="education"
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_education_title_uc"),
    )


class Skills(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    skill_group_title = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=False)

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="skills")

    built_resumes = db.relationship(
        "BuiltResume",
        secondary=built_resume_skills,
        back_populates="skills"
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_skills_title_uc"),
    )


class Language(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(128), nullable=False)
    proficiency = db.Column(db.String(128), nullable=False)

    user_id = db.Column(GUID(), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="languages")

    built_resumes = db.relationship(
        "BuiltResume",
        secondary=built_resume_language,
        back_populates="languages"
    )

    __table_args__ = (
        db.UniqueConstraint("user_id", "entry_title", name="_user_language_title_uc"),
    )


class ResumeTheme(db.Model, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False) # <-- REMOVED unique=True
    description = db.Column(db.String(200), nullable=True)
    styles = db.Column(db.Text, nullable=False)

    built_resumes = db.relationship("BuiltResume", back_populates="theme")

    __table_args__ = (
        db.UniqueConstraint('name', name='_resumetheme_name_uc'),
    )


class BuiltResume(db.Model, EntryTitleMixin, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)

    basic_info_id = db.Column(
        GUID(),
        db.ForeignKey("basic_info.id", ondelete="RESTRICT"),
        nullable=False
    )
    summary_id = db.Column(GUID(), db.ForeignKey("summary.id", ondelete="RESTRICT"), nullable=False)
    theme_id = db.Column(GUID(), db.ForeignKey("resume_theme.id", ondelete="RESTRICT"), nullable=False)

    basic_info = relationship("BasicInfo", back_populates="built_resumes")
    summary = relationship("Summary", back_populates="built_resumes")
    theme = relationship("ResumeTheme", back_populates="built_resumes")

    experience = relationship(
        "Experience", secondary=built_resume_experience, back_populates="built_resumes"
    )
    education = relationship(
        "Education", secondary=built_resume_education, back_populates="built_resumes"
    )
    skills = relationship(
        "Skills", secondary=built_resume_skills, back_populates="built_resumes"
    )
    languages = relationship(
        "Language", secondary=built_resume_language, back_populates="built_resumes"
    )

    user_id = db.Column(
        GUID(),
        db.ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    user = db.relationship("User", back_populates="resumes")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id", "entry_title", name="_user_built_resumes_title_uc"
        ),
    )

    @classmethod
    def get_active_count(cls):
        count_stmt = select(func.count(cls.id))
        return db.session.scalar(count_stmt)


class ApplicationStage(db.Model, TimeStampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    job_applications = relationship(
        "JobApplication", 
        back_populates="stage",
        passive_deletes=True
    )

    def __repr__(self):
        return f"ApplicationStage({self.id}: {self.name})"


class JobApplication(db.Model, TimeStampMixin):
    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)

    job_title = db.Column(db.String, nullable=False)
    company_name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=True)

    application_date = db.Column(db.Date, nullable=True)

    job_url = db.Column(db.String, nullable=True)
    application_source = db.Column(db.String, nullable=False)

    application_stage_id = db.Column(
        db.Integer, 
        db.ForeignKey("application_stage.id", ondelete="RESTRICT"), 
        nullable=False
    )
    stage = relationship("ApplicationStage", back_populates="job_applications")

    user_id = db.Column(
        GUID(), 
        db.ForeignKey("user.id", ondelete="CASCADE"), 
        nullable=False
    )
    user = relationship("User", back_populates="job_applications")

    def __repr__(self):
        return f"JobApplication({self.job_title} @{self.company_name})"
