from flask import Blueprint, jsonify, request
from flask_security import auth_required, hash_password
from flask_security.utils import verify_password

from extensions import db
from models import Company, Role, StudentProfile, User
from utils import normalize_role, serialize_user


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""
    role_name = normalize_role(payload.get("role") or "Student")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({"error": f"Role '{role_name}' is not available"}), 400

    user = User(email=email, password=hash_password(password), role=role_name)
    user.roles.append(role)
    db.session.add(user)
    db.session.flush()

    if role_name == "Student":
        profile = StudentProfile(
            user_id=user.id,
            name=payload.get("name") or email.split("@")[0],
            skills=payload.get("skills") or "",
            resume_url=payload.get("resume_url") or "",
            cgpa=float(payload.get("cgpa") or 0),
            branch=payload.get("branch") or "",
        )
        db.session.add(profile)
    elif role_name == "CompanyHR":
        company_name = payload.get("company_name") or payload.get("name") or "HR Company"
        company = Company(
            name=company_name,
            industry=payload.get("industry") or "",
            hr_user_id=user.id,
            description=payload.get("company_description") or "",
        )
        db.session.add(company)

    db.session.commit()
    return jsonify({"message": "Registered successfully", "user": serialize_user(user)}), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = user.get_auth_token()
    return jsonify({"token": token, "user": serialize_user(user)})
