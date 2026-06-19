import random
import string
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='Administrator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    announcements = db.relationship('Announcement', backref='author', lazy='dynamic')
    gallery_items = db.relationship('Gallery', backref='uploader', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('admin.user_id'), nullable=False)

    def __repr__(self):
        return f'<Announcement {self.title}>'


class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(200))
    event_name = db.Column(db.String(100))
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('admin.user_id'), nullable=False)

    def __repr__(self):
        return f'<Gallery {self.image_path}>'


class MatricResult(db.Model):
    __tablename__ = 'matric_results'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    candidates = db.Column(db.Integer, nullable=False)
    pass_rate = db.Column(db.Float, nullable=False)
    bachelor_passes = db.Column(db.Integer, nullable=False)
    diploma_passes = db.Column(db.Integer, nullable=False, default=0)
    higher_cert_passes = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<MatricResult {self.year}>'


class ApplicationRequest(db.Model):
    __tablename__ = 'application_requests'
    id = db.Column(db.Integer, primary_key=True)
    parent_name = db.Column(db.String(100), nullable=False)
    parent_email = db.Column(db.String(120), nullable=False)
    parent_phone = db.Column(db.String(20), nullable=False)
    learner_first_name = db.Column(db.String(50), nullable=False)
    learner_last_name = db.Column(db.String(50), nullable=False)
    current_grade = db.Column(db.String(15), nullable=False)
    grade_applying = db.Column(db.String(15), nullable=False)
    popia_consent = db.Column(db.Boolean, nullable=False, default=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_reviewed = db.Column(db.Boolean, default=False)
    reference_number = db.Column(db.String(20), unique=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')

    @staticmethod
    def generate_reference():
        chars = string.ascii_uppercase + string.digits
        suffix = ''.join(random.choices(chars, k=6))
        return f'QHS-{datetime.utcnow().year}-{suffix}'

    def __repr__(self):
        return f'<ApplicationRequest {self.reference_number}>'


class ContactSubmission(db.Model):
    __tablename__ = 'contact_submissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactSubmission {self.name}>'
