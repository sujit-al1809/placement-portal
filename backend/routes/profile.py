from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user

from extensions import db
from models import Company, StudentProfile
from utils import require_roles


profile_bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@profile_bp.get("")
@auth_required("token")
def get_profile():
    if current_user.role == "Student" and current_user.student_profile:
        return jsonify({"profile": current_user.student_profile.to_dict()})
    if current_user.role == "CompanyHR" and current_user.company:
        return jsonify({"profile": current_user.company.to_dict()})
    return jsonify({"profile": current_user.to_dict()})


@profile_bp.put("")
@auth_required("token")
def update_profile():
    payload = request.get_json(silent=True) or {}

    if current_user.role == "Student":
        profile = current_user.student_profile
        if not profile:
            profile = StudentProfile(user_id=current_user.id, name=payload.get("name") or current_user.email)
            db.session.add(profile)
        profile.name = payload.get("name", profile.name)
        profile.skills = payload.get("skills", profile.skills)
        profile.resume_url = payload.get("resume_url", profile.resume_url)
        profile.cgpa = float(payload.get("cgpa", profile.cgpa or 0))
        profile.branch = payload.get("branch", profile.branch)
    elif current_user.role == "CompanyHR":
        company = current_user.company
        if not company:
            company = Company(name=payload.get("name") or "HR Company", hr_user_id=current_user.id)
            db.session.add(company)
        company.name = payload.get("name", company.name)
        company.industry = payload.get("industry", company.industry)
        company.description = payload.get("description", company.description)
    else:
        current_user.email = payload.get("email", current_user.email)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})
