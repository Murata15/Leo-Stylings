from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='citizen')

class DocumentRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='Received')
    tracking_number = db.Column(db.String(20), unique=True, nullable=False)
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='document_requests')

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purpose = db.Column(db.String(200), nullable=False)
    schedule_date = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50), default='Pending')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='Submitted')

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, server_default=db.func.now())
    image_filename = db.Column(db.String(100), nullable=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)

class DownloadableForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
