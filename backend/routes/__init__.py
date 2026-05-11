from .admin import admin_bp
from .applications import applications_bp
from .auth import auth_bp
from .jobs import jobs_bp
from .match_score import match_score_bp
from .profile import profile_bp

__all__ = [
    "admin_bp",
    "applications_bp",
    "auth_bp",
    "jobs_bp",
    "match_score_bp",
    "profile_bp",
]
