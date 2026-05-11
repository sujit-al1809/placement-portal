from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from config import Config
from extensions import db, mail
from models import Company, Job, Role, StudentProfile, User
from routes import admin_bp, applications_bp, auth_bp, jobs_bp, match_score_bp, profile_bp
from tasks import init_celery


security = Security()
celery = None


def ensure_roles():
    roles = {
        "Student": "Student user",
        "CompanyHR": "Company human resources user",
        "Admin": "System administrator",
    }
    for name, description in roles.items():
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name, description=description))
    db.session.commit()


def create_app():
    global celery

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True)
    db.init_app(app)
    mail.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    celery = init_celery(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(match_score_bp)
    app.register_blueprint(admin_bp)

    @app.get("/")
    def health_check():
        return jsonify({"message": "Placement Portal API is running"})

    @app.after_request
    def add_headers(response):
        response.headers["Cache-Control"] = "no-store"
        return response

    with app.app_context():
        db.create_all()
        ensure_roles()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
