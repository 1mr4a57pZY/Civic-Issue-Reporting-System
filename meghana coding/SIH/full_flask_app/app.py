from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import pytz
import os
import random
import string
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "meghanachidiri2007@gmail.com"  # your Gmail
app.config['MAIL_PASSWORD'] = "shgt bavl bhgs nyja"  # App Password

mail = Mail(app)
db = SQLAlchemy(app)

# Upload folder config
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile = db.Column(db.String(20), unique=True, nullable=True)
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)

    reports = db.relationship('Report', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="pending")
    department = db.Column(db.String(100), nullable=False)
    photos = db.Column(db.Text, nullable=True)  # store filenames separated by ;
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updates = db.relationship('Update', backref='report', lazy=True)
    feedbacks = db.relationship('Feedback', backref='report', lazy=True)

class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    status = db.Column(db.String(50))
    comment = db.Column(db.Text, nullable=True)
    photos = db.Column(db.Text, nullable=True)  # filenames separated by ;
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    # Additional fields can be added here if needed

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    report_id = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    is_read = db.Column(db.Boolean, default=False)

# Send OTP email
def send_otp_email(recipient_email, otp):
    msg = Message("Your OTP Code", sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
    msg.body = f"Your OTP is {otp}. It is valid for 10 minutes."
    mail.send(msg)
    print(f"OTP sent to {recipient_email}")

# Send resolution notification email
def send_resolution_email(user, report):
    if user.email:
        try:
            msg = Message("Your reported issue has been resolved",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[user.email])
            msg.body = f"Hello {user.name},\n\nYour reported issue titled '{report.title}' has been marked as resolved. Thank you for helping improve the community.\n\nBest regards,\nCivic Report Team"
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send resolution email: {e}")

# Routes

@app.route('/')
def home():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        notifications = Notification.query.filter_by(user_id=user.id, is_read=False).all()
        reports = Report.query.filter_by(user_id=user.id).order_by(Report.created_at.desc()).all()
        return render_template('home.html', user=user, notifications=notifications, reports=reports)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        name = request.form.get('name')

        if not (mobile or email):
            flash("Please provide either mobile or email", "danger")
            return redirect(url_for('register'))

        otp = ''.join(random.choices(string.digits, k=6))

        user = User.query.filter((User.mobile == mobile) | (User.email == email)).first()
        if not user:
            user = User(name=name, email=email, mobile=mobile, otp=otp, otp_created_at=datetime.now())
            db.session.add(user)
        else:
            user.otp = otp
            user.otp_created_at = datetime.now()
        db.session.commit()

        if email:
            send_otp_email(email, otp)
        else:
            print(f"OTP for {mobile}: {otp}")

        session['pending_user'] = user.id
        return redirect(url_for('verify_otp'))
    return render_template('register.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        user_id = session.get('pending_user')
        user = User.query.get(user_id)

        if user and user.otp == otp:
            # Check OTP expiry (10 minutes)
            if datetime.now() - user.otp_created_at > timedelta(minutes=10):
                flash("OTP expired, please request a new one.", "danger")
                return redirect(url_for('register'))

            user.is_verified = True
            user.otp = None
            user.otp_created_at = None
            db.session.commit()
            session['user_id'] = user.id
            session.pop('pending_user', None)
            flash("OTP verified successfully! Please submit your report.", "success")
            return redirect(url_for('submit_report'))
        else:
            flash("Invalid OTP, try again", "danger")
    return render_template('onetimepassword.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))

@app.route('/submit', methods=['GET', 'POST'])
def submit_report():
    if "user_id" not in session:
        flash("You must log in first", "warning")
        return redirect(url_for('register'))

    user = User.query.get(session['user_id'])
    if not user or not user.is_verified:
        flash("You must verify your account before submitting reports.", "warning")
        return redirect(url_for('verify_otp'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        department = request.form.get('department') or "General"

        # Validate mandatory fields
        if not title or not description or not location or not department:
            flash("All fields (Title, Description, Location, Department) are mandatory.", "danger")
            return redirect(url_for('submit_report'))

        # Handle photo uploads
        photos = []
        if 'photo' in request.files:
            files = request.files.getlist('photo')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    filename = f"{timestamp}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    photos.append(filename)

        photos_str = ';'.join(photos) if photos else None

        report = Report(
            title=title,
            description=description,
            location=location,
            department=department,
            photos=photos_str,
            user_id=user.id
        )
        db.session.add(report)
        db.session.commit()
        flash("Report submitted successfully", "success")
        return redirect(url_for('home'))

    return render_template('submit_report.html')

@app.route('/admin')
def admin_dashboard():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    return render_template('admin.html', reports=reports)

@app.route('/admin/report/<int:report_id>', methods=['GET', 'POST'])
def admin_report_detail(report_id):
    report = Report.query.get_or_404(report_id)

    if request.method == 'POST':
        status = request.form.get('status')
        comment = request.form.get('comment')
        photos = request.files.getlist('photo')

        # Update report status
        previous_status = report.status
        report.status = status

        # Save update photos
        update_photos = []
        for file in photos:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                update_photos.append(filename)
        photos_str = ';'.join(update_photos) if update_photos else None

        # Create update entry
        update = Update(
            report_id=report.id,
            status=status,
            comment=comment,
            photos=photos_str
        )
        db.session.add(update)
        db.session.commit()

        # Send notification if status changed to resolved
        if status == 'resolved' and previous_status != 'resolved':
            user = report.user
            if user:
                # Create notification entry
                notification = Notification(
                    user_id=user.id,
                    report_id=report.id,
                    message=f"Your reported issue '{report.title}' has been resolved."
                )
                db.session.add(notification)
                db.session.commit()

                # Send email notification
                send_resolution_email(user, report)

        flash("Report updated successfully", "success")
        return redirect(url_for('admin_report_detail', report_id=report_id))

    updates = Update.query.filter_by(report_id=report.id).order_by(Update.created_at.desc()).all()
    # Pass the translation dictionary 't' to the template to fix the undefined error
    t = {
        "admin_portal": "Admin Portal",
        "location": "Location",
        "department": "Department",
        "submitted": "Submitted",
        "pending": "Pending",
        "acknowledged": "Acknowledged",
        "in_progress": "In Progress",
        "resolved": "Resolved",
        "report_photo": "Report Photos",
        "update_status": "Update Status",
        "status": "Status",
        "comment": "Comment",
        "upload_photos": "Upload Photos",
        "save_update": "Save Update",
        "past_updates": "Past Updates",
        "user_feedbacks": "User Feedbacks",
        "give_feedback": "Give Feedback",
        "submit_feedback": "Submit Feedback"
    }
    return render_template('admin_report_detail.html', report=report, updates=updates, t=t)

@app.route('/notifications')
def notifications():
    if 'user_id' not in session:
        flash("You must log in first", "warning")
        return redirect(url_for('register'))

    user = User.query.get(session['user_id'])
    notifications = Notification.query.filter_by(user_id=user.id, is_read=False).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/notifications/mark_read/<int:notification_id>')
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('notifications'))

@app.route('/report/<int:report_id>/feedback', methods=['POST'])
def submit_feedback(report_id):
    report = Report.query.get_or_404(report_id)
    rating = int(request.form.get('rating', 0))
    comment = request.form.get('comment')

    if rating < 1 or rating > 5:
        flash("Invalid rating value.", "danger")
        return redirect(url_for('status', report_id=report_id))

    feedback = Feedback(
        report_id=report.id,
        rating=rating,
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()
    flash("Thank you for your feedback!", "success")
    return redirect(url_for('status', report_id=report_id))

@app.route('/status/<int:report_id>')
def status(report_id):
    report = Report.query.get_or_404(report_id)
    feedbacks = Feedback.query.filter_by(report_id=report.id).order_by(Feedback.created_at.desc()).all()
    return render_template('status.html', report=report, feedbacks=feedbacks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
