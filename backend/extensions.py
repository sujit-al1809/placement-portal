from celery import Celery
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mail = Mail()
celery = Celery(__name__)
