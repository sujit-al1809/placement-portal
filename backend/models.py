from datetime import datetime
from uuid import uuid4

from flask_security import RoleMixin, UserMixin

from extensions import db


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid4()))
    role = db.Column(db.String(32), nullable=False, default="Student")

    roles = db.relationship("Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic"))
    student_profile = db.relationship("StudentProfile", back_populates="user", uselist=False)
    company = db.relationship("Company", back_populates="hr_user", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "active": self.active,
        }


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    skills = db.Column(db.Text, default="")
    resume_url = db.Column(db.String(512), default="")
    cgpa = db.Column(db.Float, default=0.0)
    branch = db.Column(db.String(120), default="")

    user = db.relationship("User", back_populates="student_profile")
    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "skills": self.skills,
            "resume_url": self.resume_url,
            "cgpa": self.cgpa,
            "branch": self.branch,
            "email": self.user.email if self.user else None,
        }


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(120), default="")
    hr_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    description = db.Column(db.Text, default="")

    hr_user = db.relationship("User", back_populates="company")
    jobs = db.relationship("Job", back_populates="company", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "hr_user_id": self.hr_user_id,
            "hr_email": self.hr_user.email if self.hr_user else None,
            "description": self.description,
        }


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text, default="")
    package = db.Column(db.String(80), default="")
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    company = db.relationship("Company", back_populates="jobs")
    applications = db.relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company.name if self.company else None,
            "title": self.title,
            "description": self.description,
            "required_skills": self.required_skills,
            "package": self.package,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_profile.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    status = db.Column(db.String(40), default="Applied", nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    match_score = db.Column(db.Float, default=0.0)

    student = db.relationship("StudentProfile", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

    __table_args__ = (db.UniqueConstraint("student_id", "job_id", name="uq_student_job"),)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.name if self.student else None,
            "job_id": self.job_id,
            "job_title": self.job.title if self.job else None,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "match_score": self.match_score,
        }
