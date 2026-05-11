from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user

from extensions import db
from models import Job
from tasks import notify_matching_students
from utils import require_roles


jobs_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


@jobs_bp.get("")
@auth_required("token")
def list_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return jsonify({"jobs": [job.to_dict() for job in jobs]})


@jobs_bp.post("")
@auth_required("token")
@require_roles("CompanyHR", "Admin")
def create_job():
    payload = request.get_json(silent=True) or {}
    company = current_user.company if current_user.role == "CompanyHR" else None
    company_id = payload.get("company_id") or (company.id if company else None)
    if not company_id:
        return jsonify({"error": "company_id is required"}), 400

    deadline_raw = payload.get("deadline")
    try:
        deadline = datetime.fromisoformat(deadline_raw) if deadline_raw else datetime.utcnow()
    except ValueError:
        return jsonify({"error": "deadline must be an ISO-8601 datetime string"}), 400

    job = Job(
        company_id=company_id,
        title=payload.get("title") or "",
        description=payload.get("description") or "",
        required_skills=payload.get("required_skills") or "",
        package=payload.get("package") or "",
        deadline=deadline,
    )
    db.session.add(job)
    db.session.commit()

    notify_matching_students.delay(job.id)
    return jsonify({"message": "Job created", "job": job.to_dict()}), 201


@jobs_bp.get("/<int:job_id>")
@auth_required("token")
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify({"job": job.to_dict()})


@jobs_bp.put("/<int:job_id>")
@auth_required("token")
@require_roles("CompanyHR", "Admin")
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.role == "CompanyHR" and job.company.hr_user_id != current_user.id:
        return jsonify({"error": "You can only edit jobs from your company"}), 403

    payload = request.get_json(silent=True) or {}
    job.title = payload.get("title", job.title)
    job.description = payload.get("description", job.description)
    job.required_skills = payload.get("required_skills", job.required_skills)
    job.package = payload.get("package", job.package)
    if payload.get("deadline"):
        job.deadline = datetime.fromisoformat(payload["deadline"])

    db.session.commit()
    return jsonify({"message": "Job updated", "job": job.to_dict()})


@jobs_bp.delete("/<int:job_id>")
@auth_required("token")
@require_roles("CompanyHR", "Admin")
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if current_user.role == "CompanyHR" and job.company.hr_user_id != current_user.id:
        return jsonify({"error": "You can only delete jobs from your company"}), 403

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"})


@jobs_bp.post("/<int:job_id>/apply")
@auth_required("token")
@require_roles("Student")
def apply_to_job(job_id):
    from models import Application

    job = Job.query.get_or_404(job_id)
    student_profile = current_user.student_profile
    if not student_profile:
        return jsonify({"error": "Student profile not found"}), 404

    existing = Application.query.filter_by(student_id=student_profile.id, job_id=job.id).first()
    if existing:
        return jsonify({"error": "You have already applied for this job"}), 409

    application = Application(student_id=student_profile.id, job_id=job.id)
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Application submitted", "application": application.to_dict()}), 201
