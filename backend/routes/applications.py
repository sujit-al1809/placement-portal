from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user

from extensions import db
from models import Application, Company, Job
from services.matching import calculate_match_score
from utils import require_roles


applications_bp = Blueprint("applications", __name__, url_prefix="/api/applications")


@applications_bp.get("")
@auth_required("token")
def list_applications():
    if current_user.role == "Student":
        student_profile = current_user.student_profile
        query = Application.query.filter_by(student_id=student_profile.id) if student_profile else Application.query.filter_by(id=-1)
    elif current_user.role == "CompanyHR":
        query = (
            Application.query.join(Application.job)
            .join(Job.company)
            .filter(Company.hr_user_id == current_user.id)
        )
    else:
        query = Application.query

    applications = query.order_by(Application.applied_at.desc()).all()
    return jsonify({"applications": [application.to_dict() for application in applications]})


@applications_bp.put("/<int:application_id>/status")
@auth_required("token")
@require_roles("CompanyHR", "Admin")
def update_application_status(application_id):
    application = Application.query.get_or_404(application_id)
    if current_user.role == "CompanyHR" and application.job.company.hr_user_id != current_user.id:
        return jsonify({"error": "You can only update applications for your company"}), 403

    payload = request.get_json(silent=True) or {}
    status = (payload.get("status") or "").strip()
    if not status:
        return jsonify({"error": "status is required"}), 400

    application.status = status
    db.session.commit()
    return jsonify({"message": "Application status updated", "application": application.to_dict()})
