from flask import Blueprint, jsonify, request
from flask_security import auth_required

from extensions import db
from models import Company, Role, User
from utils import require_roles, serialize_user


admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/users")
@auth_required("token")
@require_roles("Admin")
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify({"users": [serialize_user(user) for user in users]})


@admin_bp.put("/users/<int:user_id>")
@auth_required("token")
@require_roles("Admin")
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    payload = request.get_json(silent=True) or {}
    if payload.get("role"):
        role_name = payload["role"]
        role = Role.query.filter_by(name=role_name).first()
        if role and role not in user.roles:
            user.roles = [role]
        user.role = role_name
    if "active" in payload:
        user.active = bool(payload["active"])
    db.session.commit()
    return jsonify({"message": "User updated", "user": serialize_user(user)})


@admin_bp.get("/companies")
@auth_required("token")
@require_roles("Admin")
def list_companies():
    companies = Company.query.order_by(Company.id.asc()).all()
    return jsonify({"companies": [company.to_dict() for company in companies]})


@admin_bp.post("/companies")
@auth_required("token")
@require_roles("Admin")
def create_company():
    payload = request.get_json(silent=True) or {}
    hr_user_id = payload.get("hr_user_id")
    if not hr_user_id:
        return jsonify({"error": "hr_user_id is required"}), 400

    company = Company(
        name=payload.get("name") or "",
        industry=payload.get("industry") or "",
        hr_user_id=hr_user_id,
        description=payload.get("description") or "",
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({"message": "Company created", "company": company.to_dict()}), 201
