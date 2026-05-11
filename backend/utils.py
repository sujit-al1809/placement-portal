from functools import wraps

from flask import jsonify
from flask_security import current_user


ROLE_ALIASES = {
    "companyhr": "CompanyHR",
    "company_hr": "CompanyHR",
    "student": "Student",
    "admin": "Admin",
}


def normalize_role(role_name: str) -> str:
    return ROLE_ALIASES.get(role_name.lower(), role_name)


def user_role_names(user):
    return {role.name for role in getattr(user, "roles", [])}


def primary_role(user):
    return getattr(user, "role", "Student")


def serialize_user(user):
    payload = user.to_dict()
    payload["roles"] = sorted(user_role_names(user))
    if user.student_profile:
        payload["student_profile"] = user.student_profile.to_dict()
    if user.company:
        payload["company"] = user.company.to_dict()
    return payload


def require_roles(*allowed_roles):
    allowed = {normalize_role(role) for role in allowed_roles}

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "Authentication required"}), 401
            roles = user_role_names(current_user) | {primary_role(current_user)}
            if not roles.intersection(allowed):
                return jsonify({"error": "You do not have permission to access this resource"}), 403
            return view(*args, **kwargs)

        return wrapped

    return decorator
