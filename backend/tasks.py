import logging

from flask import current_app
from flask_mail import Message

from extensions import celery, db, mail
from models import Application, Job, StudentProfile
from services.matching import calculate_match_score

logger = logging.getLogger(__name__)


def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@celery.task(name="notify_matching_students")
def notify_matching_students(job_id):
    job = Job.query.get(job_id)
    if not job:
        return {"sent": 0, "reason": "job-not-found"}

    sent_to = []
    students = StudentProfile.query.all()
    for student in students:
        score, _ = calculate_match_score(student.skills, job.description)
        if score <= 60:
            continue

        recipient = student.user.email if student.user else None
        if not recipient:
            continue

        subject = f"New matching job: {job.title}"
        body = (
            f"Hi {student.name},\n\n"
            f"A new job '{job.title}' from {job.company.name if job.company else 'a company'} matches your profile with a score of {score}%.\n"
            f"Apply before {job.deadline.strftime('%Y-%m-%d') if job.deadline else 'the deadline'}.\n"
        )

        try:
            if current_app.config.get("MAIL_SUPPRESS_SEND", True):
                logger.info("Email alert suppressed for %s", recipient)
            else:
                mail.send(Message(subject=subject, recipients=[recipient], body=body))
            sent_to.append({"email": recipient, "match_score": score})
        except Exception as exc:
            logger.exception("Failed to send alert to %s", recipient)
            sent_to.append({"email": recipient, "error": str(exc)})

    return {"sent": len(sent_to), "recipients": sent_to}
