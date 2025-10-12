import os


class ConfigMissingSecretKey(Exception):
    """Exception for missing SECRET_KEY environment variable."""


class Config:
    FEATURE_FLAGS = {"registration_enabled": True, "register_with_invite_code": False}
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///resume_builder.db"
    )
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ConfigMissingSecretKey


class ProductionConfig(Config):
    FEATURE_FLAGS = Config.FEATURE_FLAGS.copy()
    FEATURE_FLAGS.update(
        {
            "registration_enabled": False,
            "register_with_invite_code": os.getenv(
                "REGISTRATION_WITH_INVITE_CODE", "True"
            ).lower()
            == "true",
        }
    )
    SQLALCHEMY_ECHO = False
    FLASK_DEBUG = False


class DevelopmentConfig(Config):
    FEATURE_FLAGS = Config.FEATURE_FLAGS.copy()
    FEATURE_FLAGS.update(
        {
            "registration_enabled": os.getenv("REGISTRATION_ENABLED", "True").lower()
            == "true",
            "register_with_invite_code": os.getenv(
                "REGISTRATION_WITH_INVITE_CODE", "True"
            ).lower()
            == "true",
        }
    )
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"


config_by_env = {"development": DevelopmentConfig, "production": ProductionConfig}
