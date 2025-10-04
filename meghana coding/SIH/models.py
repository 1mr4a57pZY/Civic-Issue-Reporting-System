from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    otp = db.Column(db.String(6), nullable=True)  # temporary storage
    otp_created_at = db.Column(db.DateTime, nullable=True)  # OTP creation time
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    # Relationships
    reports = db.relationship('Report', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=True)  # GPS latitude coordinate
    longitude = db.Column(db.Float, nullable=True)  # GPS longitude coordinate
    status = db.Column(db.String(50), default="pending")
    department = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(1000), nullable=True)  # Legacy field for backward compatibility
    media = db.Column(db.String(2000), nullable=True)  # New field for multiple media files
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')),
                          onupdate=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    updates = db.relationship('Update', backref='report', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='report', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Report {self.title}>'


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(1000), nullable=True)  # Store filenames separated by ';'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return f'<Update {self.id}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return f'<Notification {self.id}>'


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating scale
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return f'<Feedback {self.id}>'
