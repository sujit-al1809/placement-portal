import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{INSTANCE_DIR / 'placement_portal.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "dev-password-salt")
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_REGISTERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_MAX_AGE = None
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = True

    JWT = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@placement-portal.local")
    MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", "true").lower() == "true"

    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
