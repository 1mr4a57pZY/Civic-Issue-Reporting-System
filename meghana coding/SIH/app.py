from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_babel import Babel, gettext as _
from flask_migrate import Migrate
from datetime import datetime
import pytz, os, random
from werkzeug.utils import secure_filename
from geocoding import geocode_with_retry
from utils import serialize_reports

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'meghanachidiri2007@gmail.com'
app.config['MAIL_PASSWORD'] = 'shgt bavl bhgs nyja'

db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)
migrate = Migrate(app, db)

# Translations dictionary for multi-language support
translations = {
    'en': {
        "dashboard": "Dashboard",
        "submit_report": "Submit Report",
        "admin_portal": "Admin Portal",
        "location": "Location",
        "department": "Department",
        "submitted": "Submitted",
        "view_details": "View Details",
        "report_a_civic_issue": "Report a Civic Issue",
        "issue_title": "Issue Title",
        "brief_description": "Brief description of the issue",
        "keep_concise": "Keep it concise and clear",
        "detailed_description": "Detailed Description",
        "provide_detailed_info": "Provide detailed information about the issue",
        "include_detail_help": "Include any relevant details that might help resolve the issue",
        "street_address_landmark": "Street address or landmark",
        "be_specific_help": "Be as specific as possible to help locate the issue",
        "select_department": "Select Department",
        "select_appropriate_dept": "Select the most appropriate department for this issue",
        "upload_photos": "Upload Photos",
        "optional": "Optional",
        "click_upload_photos": "Click to upload photos",
        "multiple_files_supported": "Multiple files supported",
        "cancel": "Cancel",
        "help_improve_community": "Help improve your community by reporting civic issues",
        "admin_dashboard": "Admin Dashboard",
        "back_to_user_portal": "← Back to User Portal",
        "total_reports": "Total Reports",
        "pending": "Pending",
        "in_progress": "In Progress",
        "resolved": "Resolved",
        "view_full_details": "View Full Details",
        "no_reports_yet": "No Reports Yet",
        "dashboard_description": "The dashboard will show all submitted civic reports here.",
        "admin_portal": "Admin Portal",
        "acknowledged": "Acknowledged",
        "report_photo": "Report Photo",
        "update_status": "Update Status",
        "comment": "Comment",
        "upload_photos_plural": "Upload Photos",
        "save_update": "Save Update",
        "past_updates": "Past Updates",
        "user_feedbacks": "User Feedbacks",
        "give_feedback": "Give Feedback",
        "your_feedback": "Your Feedback",
        "submit_feedback": "Submit Feedback",
        "report_details": "Report Details",
        "description": "Description",
        "contact_number": "Contact Number",
        "current_status": "Current Status",
        "update_report": "Update Report",
        "status_updates_progress": "Status Updates & Progress",
        "share_feedback": "Share Your Feedback",
        "rate_experience": "Rate your experience:",
        "additional_comments": "Additional Comments (Optional):",
        "submit_feedback_btn": "Submit Feedback",
        "notifications": "Notifications",
        "no_new_notifications": "No new notifications.",
        "mark_as_read": "Mark as Read",
        "back_to_home": "Back to Home",
        "verify_account": "Verify Account",
        "account_verified": "✓ Account Verified",
        "account_not_verified": "⚠ Account Not Verified",
        "logged_out_successfully": "Logged out successfully",
        "otp_verified_successfully": "OTP verified successfully! Please submit your report.",
        "invalid_otp_try_again": "Invalid OTP, try again",
        "must_log_in_first": "You must log in first",
        "must_verify_before_submit": "You must verify your account before submitting reports.",
        "all_fields_mandatory": "All fields (Title, Description, Location, Department) are mandatory.",
        "file_too_large": "File {filename} is too large. Maximum size is 20MB.",
        "report_submitted_successfully": "Report submitted successfully",
        "report_updated_successfully": "Report updated successfully",
        "feedback_submitted_successfully": "Feedback submitted successfully",
        "language_switched": "Language switched to {lang}",
        "please_provide_mobile_or_email": "Please provide either mobile or email"
    },
    'hi': {
        "dashboard": "डैशबोर्ड",
        "submit_report": "रिपोर्ट सबमिट करें",
        "admin_portal": "प्रशासन पोर्टल",
        "location": "स्थान",
        "department": "विभाग",
        "submitted": "सबमिट किया गया",
        "view_details": "विवरण देखें",
        "report_a_civic_issue": "नागरिक समस्या रिपोर्ट करें",
        "issue_title": "समस्या का शीर्षक",
        "brief_description": "समस्या का संक्षिप्त विवरण",
        "keep_concise": "संक्षिप्त और स्पष्ट रखें",
        "detailed_description": "विस्तृत विवरण",
        "provide_detailed_info": "समस्या के बारे में विस्तृत जानकारी प्रदान करें",
        "include_detail_help": "कोई भी प्रासंगिक विवरण शामिल करें जो समस्या को हल करने में मदद कर सकता है",
        "street_address_landmark": "सड़क का पता या लैंडमार्क",
        "be_specific_help": "समस्या का स्थान खोजने में मदद के लिए यथासंभव विशिष्ट रहें",
        "select_department": "विभाग चुनें",
        "select_appropriate_dept": "इस समस्या के लिए सबसे उपयुक्त विभाग चुनें",
        "upload_photos": "फोटो अपलोड करें",
        "optional": "वैकल्पिक",
        "click_upload_photos": "फोटो अपलोड करने के लिए क्लिक करें",
        "multiple_files_supported": "कई फाइलें समर्थित हैं",
        "cancel": "रद्द करें",
        "help_improve_community": "नागरिक समस्याओं की रिपोर्ट करके अपने समुदाय को बेहतर बनाएं",
        "admin_dashboard": "प्रशासन डैशबोर्ड",
        "back_to_user_portal": "← उपयोगकर्ता पोर्टल पर वापस जाएं",
        "total_reports": "कुल रिपोर्ट",
        "pending": "लंबित",
        "in_progress": "प्रगति पर",
        "resolved": "सुलझा हुआ",
        "view_full_details": "पूर्ण विवरण देखें",
        "no_reports_yet": "कोई रिपोर्ट नहीं",
        "dashboard_description": "डैशबोर्ड में सभी सबमिट की गई नागरिक रिपोर्ट दिखाई जाएंगी।",
        "admin_portal": "प्रशासन पोर्टल",
        "acknowledged": "स्वीकृत",
        "report_photo": "रिपोर्ट फोटो",
        "update_status": "स्थिति अपडेट करें",
        "comment": "टिप्पणी",
        "upload_photos_plural": "फोटो अपलोड करें",
        "save_update": "अपडेट सहेजें",
        "past_updates": "पिछले अपडेट",
        "user_feedbacks": "उपयोगकर्ता प्रतिक्रिया",
        "give_feedback": "प्रतिक्रिया दें",
        "your_feedback": "आपकी प्रतिक्रिया",
        "submit_feedback": "प्रतिक्रिया सबमिट करें",
        "report_details": "रिपोर्ट विवरण",
        "description": "विवरण",
        "contact_number": "संपर्क नंबर",
        "current_status": "वर्तमान स्थिति",
        "update_report": "रिपोर्ट अपडेट करें",
        "status_updates_progress": "स्थिति अपडेट और प्रगति",
        "share_feedback": "अपनी प्रतिक्रिया साझा करें",
        "rate_experience": "अपने अनुभव को रेट करें:",
        "additional_comments": "अतिरिक्त टिप्पणियाँ (वैकल्पिक):",
        "submit_feedback_btn": "प्रतिक्रिया सबमिट करें",
        "notifications": "सूचनाएं",
        "no_new_notifications": "कोई नई सूचनाएं नहीं।",
        "mark_as_read": "पढ़ा हुआ चिह्नित करें",
        "back_to_home": "होम पर वापस जाएं",
        "verify_account": "खाता सत्यापित करें",
        "account_verified": "✓ खाता सत्यापित",
        "account_not_verified": "⚠ खाता सत्यापित नहीं",
        "logged_out_successfully": "सफलतापूर्वक लॉग आउट हुआ",
        "otp_verified_successfully": "OTP सफलतापूर्वक सत्यापित! कृपया अपनी रिपोर्ट सबमिट करें।",
        "invalid_otp_try_again": "अमान्य OTP, पुनः प्रयास करें",
        "must_log_in_first": "पहले आपको लॉग इन करना होगा",
        "must_verify_before_submit": "रिपोर्ट सबमिट करने से पहले आपको अपना खाता सत्यापित करना होगा।",
        "all_fields_mandatory": "सभी फ़ील्ड (शीर्षक, विवरण, स्थान, विभाग) अनिवार्य हैं।",
        "file_too_large": "फ़ाइल {filename} बहुत बड़ी है। अधिकतम आकार 20MB है।",
        "report_submitted_successfully": "रिपोर्ट सफलतापूर्वक सबमिट हुई",
        "report_updated_successfully": "रिपोर्ट सफलतापूर्वक अपडेट हुई",
        "feedback_submitted_successfully": "प्रतिक्रिया सफलतापूर्वक सबमिट हुई",
        "language_switched": "भाषा {lang} में बदल गई"
    },
    'te': {
        "dashboard": "డాష్‌బోర్డ్",
        "submit_report": "రిపోర్ట్ సమర్పించండి",
        "admin_portal": "అడ్మిన్ పోర్టల్",
        "location": "స్థానం",
        "department": "విభాగం",
        "submitted": "సమర్పించబడింది",
        "view_details": "వివరాలు చూడండి",
        "report_a_civic_issue": "పౌర సమస్యను నివేదించండి",
        "issue_title": "సమస్య శీర్షిక",
        "brief_description": "సమస్య యొక్క సంక్షిప్త వివరణ",
        "keep_concise": "సంక్షిప్తంగా మరియు స్పష్టంగా ఉంచండి",
        "detailed_description": "వివరమైన వివరణ",
        "provide_detailed_info": "సమస్య గురించి వివరమైన సమాచారం ఇవ్వండి",
        "include_detail_help": "సమస్యను పరిష్కరించడంలో సహాయపడే సంబంధిత వివరాలను చేర్చండి",
        "street_address_landmark": "వీధి చిరునామా లేదా ల్యాండ్‌మార్క్",
        "be_specific_help": "సమస్యను గుర్తించడంలో సహాయపడేందుకు సాధ్యమైనంత స్పష్టంగా ఉండండి",
        "select_department": "విభాగం ఎంచుకోండి",
        "select_appropriate_dept": "ఈ సమస్యకు సరైన విభాగాన్ని ఎంచుకోండి",
        "upload_photos": "ఫోటోలు అప్‌లోడ్ చేయండి",
        "optional": "ఐచ్ఛికం",
        "click_upload_photos": "ఫోటోలు అప్‌లోడ్ చేయడానికి క్లిక్ చేయండి",
        "multiple_files_supported": "బహుళ ఫైళ్ళు మద్దతు",
        "cancel": "రద్దు చేయండి",
        "help_improve_community": "పౌర సమస్యలను నివేదించడం ద్వారా మీ సమాజాన్ని మెరుగుపరచండి",
        "admin_dashboard": "అడ్మిన్ డాష్‌బోర్డ్",
        "back_to_user_portal": "← యూజర్ పోర్టల్‌కు తిరిగి వెళ్ళండి",
        "total_reports": "మొత్తం రిపోర్టులు",
        "pending": "పెండింగ్",
        "in_progress": "ప్రగతిలో ఉంది",
        "resolved": "పరిష్కరించబడింది",
        "view_full_details": "పూర్తి వివరాలు చూడండి",
        "no_reports_yet": "ఇంకా రిపోర్టులు లేవు",
        "dashboard_description": "డాష్‌బోర్డ్‌లో సమర్పించిన అన్ని పౌర రిపోర్టులు చూపబడతాయి.",
        "admin_portal": "అడ్మిన్ పోర్టల్",
        "acknowledged": "గమనించబడింది",
        "report_photo": "రిపోర్ట్ ఫోటో",
        "update_status": "స్థితిని నవీకరించండి",
        "comment": "వ్యాఖ్య",
        "upload_photos_plural": "ఫోటోలు అప్‌లోడ్ చేయండి",
        "save_update": "నవీకరణను సేవ్ చేయండి",
        "past_updates": "గత నవీకరణలు",
        "user_feedbacks": "వినియోగదారు అభిప్రాయాలు",
        "give_feedback": "అభిప్రాయం ఇవ్వండి",
        "your_feedback": "మీ అభిప్రాయం",
        "submit_feedback": "అభిప్రాయం సమర్పించండి",
        "report_details": "రిపోర్ట్ వివరాలు",
        "description": "వివరణ",
        "contact_number": "సంప్రదింపు సంఖ్య",
        "current_status": "ప్రస్తుత స్థితి",
        "update_report": "రిపోర్ట్‌ను నవీకరించండి",
        "status_updates_progress": "స్థితి నవీకరణలు & పురోగతి",
        "share_feedback": "మీ అభిప్రాయాన్ని పంచుకోండి",
        "rate_experience": "మీ అనుభవాన్ని రేట్ చేయండి:",
        "additional_comments": "అదనపు వ్యాఖ్యలు (ఐచ్ఛికం):",
        "submit_feedback_btn": "అభిప్రాయం సమర్పించండి",
        "notifications": "నోటిఫికేషన్లు",
        "no_new_notifications": "కొత్త నోటిఫికేషన్లు లేవు.",
        "mark_as_read": "వాచ్చినట్లు గుర్తించండి",
        "back_to_home": "హోమ్‌కు తిరిగి వెళ్ళండి",
        "verify_account": "ఖాతాను ధృవీకరించండి",
        "account_verified": "✓ ఖాతా ధృవీకరించబడింది",
        "account_not_verified": "⚠ ఖాతా ధృవీకరించబడలేదు",
        "logged_out_successfully": "వెళ్ళిపోయారు",
        "otp_verified_successfully": "OTP విజయవంతంగా ధృవీకరించబడింది! దయచేసి మీ రిపోర్ట్‌ను సమర్పించండి.",
        "invalid_otp_try_again": "చెల్లని OTP, మళ్లీ ప్రయత్నించండి",
        "must_log_in_first": "ముందుగా లాగిన్ కావాలి",
        "must_verify_before_submit": "రిపోర్ట్ సమర్పించే ముందు మీ ఖాతాను ధృవీకరించాలి.",
        "all_fields_mandatory": "అన్ని ఫీల్డులు (శీర్షిక, వివరణ, స్థానం, విభాగం) తప్పనిసరి.",
        "file_too_large": "ఫైల్ {filename} చాలా పెద్దది. గరిష్ట పరిమాణం 20MB.",
        "report_submitted_successfully": "రిపోర్ట్ విజయవంతంగా సమర్పించబడింది",
        "report_updated_successfully": "రిపోర్ట్ విజయవంతంగా నవీకరించబడింది",
        "feedback_submitted_successfully": "అభిప్రాయం విజయవంతంగా సమర్పించబడింది",
        "language_switched": "భాష {lang} కు మార్చబడింది"
    }
}

def get_locale():
    return session.get('language', 'en')

Babel.localeselector = get_locale

def send_otp_email(recipient_email, otp):
    try:
        msg = Message("Your OTP Code", sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
        msg.body = f"Your OTP is {otp}. It is valid for 5 minutes."
        mail.send(msg)
        print(f"OTP sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        # Fallback: print OTP for demo
        print(f"OTP for {recipient_email}: {otp}")

@app.route('/')
def home():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('home.html', text=text, user=user)

# ================== MODELS ==================
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
    photo = db.Column(db.String(1000), nullable=True)
    media = db.Column(db.String(2000), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')),
                          onupdate=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updates = db.relationship('Update', backref='report', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='report', lazy=True, cascade='all, delete-orphan')


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    photo = db.Column(db.String(1000), nullable=True)  # Store filenames separated by ';'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))


# ================== AUTH ROUTES ==================
@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        name = request.form.get('name')

        if not (mobile or email):
            flash(text["please_provide_mobile_or_email"], "danger")
            return redirect(url_for('register'))

        otp = str(random.randint(100000, 999999))  # generate 6-digit OTP

        session['otp'] = otp
        session['email'] = email
        session['mobile'] = mobile
        session['name'] = name

        return redirect(url_for('send_otp'))
    return render_template('register.html', text=text)


@app.route('/send_otp')
def send_otp():
    otp = session.get('otp')
    email = session.get('email')
    mobile = session.get('mobile')
    name = session.get('name')
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])

    if not otp or not (email or mobile):
        flash(text["please_provide_mobile_or_email"], "danger")
        return redirect(url_for('register'))

    if email:
        send_otp_email(email, otp)
    else:
        print(f"OTP for {mobile}: {otp}")  # For demo, log OTP for mobile

    return render_template('onetimepassword.html', text=text)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    if request.method == 'POST':
        otp_parts = [request.form.get(f'otp{i}') for i in range(1, 7)]
        if not all(otp_parts) or not all(p.isdigit() for p in otp_parts):
            flash(text["invalid_otp_try_again"], "danger")
            return redirect(url_for('send_otp'))
        otp = ''.join(otp_parts)
        session_otp = session.get('otp')
        email = session.get('email')
        mobile = session.get('mobile')
        name = session.get('name')

        if otp == session_otp:
            user = None
            if email:
                user = User.query.filter_by(email=email).first()
            elif mobile:
                user = User.query.filter_by(mobile=mobile).first()

            if not user:
                user = User(name=name, email=email, mobile=mobile, is_verified=True)
                db.session.add(user)
            else:
                user.is_verified = True
            db.session.commit()

            session['user_id'] = user.id
            session.pop('otp', None)
            session.pop('email', None)
            session.pop('mobile', None)
            session.pop('name', None)

            flash(text["otp_verified_successfully"], "success")
            return redirect(url_for('submit_report'))
        else:
            flash(text["invalid_otp_try_again"], "danger")
    return render_template('onetimepassword.html', text=text)


@app.route('/logout')
def logout():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    session.clear()
    flash(text["logged_out_successfully"], "info")
    return redirect(url_for('home'))

@app.route('/set_language', methods=['POST'])
def set_language():
    lang = request.form.get("language")
    session["language"] = lang
    text = translations.get(lang, translations['en'])
    flash(text["language_switched"].format(lang=lang), "info")
    return redirect(request.referrer or url_for('home'))

@app.route('/admin')
def admin_dashboard():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    reports = Report.query.all()
    # Convert SQLAlchemy objects to JSON-serializable dictionaries
    serialized_reports = serialize_reports(reports)
    return render_template('admin.html', reports=serialized_reports, text=text)

from flask import request

@app.route('/admin/report/<int:report_id>', methods=['GET', 'POST'])
def admin_report_detail(report_id):
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    report = Report.query.get_or_404(report_id)

    if request.method == 'POST':
        status = request.form.get('status')
        comment = request.form.get('comment')
        photos = request.files.getlist('photo')

        # Update report status
        report.status = status

        # Handle photo uploads
        photo_filenames = []
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        for photo in photos:
            if photo and photo.filename:
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                filename = f"{timestamp}_{secure_filename(photo.filename)}"
                photo.save(os.path.join(upload_folder, filename))
                photo_filenames.append(filename)

        photo_str = ';'.join(photo_filenames) if photo_filenames else None

        # Create Update record
        update = Update(
            report_id=report_id,
            status=status,
            comment=comment,
            photo=photo_str
        )
        db.session.add(update)

        # If status is resolved, create Notification and send email
        if status == 'resolved':
            user = report.user
            notification = Notification(
                user_id=user.id,
                message=f"Your report '{report.title}' has been resolved."
            )
            db.session.add(notification)

            if user and user.email:
                try:
                    msg = Message("Your reported issue has been resolved",
                                  sender=app.config['MAIL_USERNAME'],
                                  recipients=[user.email])
                    msg.body = f"Hello {user.name},\n\nYour reported issue titled '{report.title}' has been marked as resolved. Thank you for helping improve the community.\n\nBest regards,\nCivic Report Team"
                    mail.send(msg)
                except Exception as e:
                    print(f"Failed to send resolution email: {e}")

        db.session.commit()

        flash(text["report_updated_successfully"], "success")
        return redirect(url_for('admin_report_detail', report_id=report_id))

    return render_template('admin_report_detail.html', report=report, text=text)

@app.route('/submit_feedback/<int:report_id>', methods=['POST'])
def submit_feedback(report_id):
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    report = Report.query.get_or_404(report_id)
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    feedback = Feedback(
        report_id=report_id,
        rating=int(rating),
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()

    flash(text["feedback_submitted_successfully"], "success")
    return redirect(url_for('admin_report_detail', report_id=report_id))

# ================== SUBMIT REPORT ==================
@app.route('/submit', methods=['GET', 'POST'])
def submit_report():
    lang = session.get('language', 'en')
    text = translations.get(lang, translations['en'])
    if "user_id" not in session:
        flash(text["must_log_in_first"], "warning")
        return redirect(url_for('register'))

    user = User.query.get(session['user_id'])
    if not user or not user.is_verified:
        flash(text["must_verify_before_submit"], "warning")
        return redirect(url_for('verify_otp'))

    if request.method == 'POST':
        title = request.form.get('title')
        short_description = request.form.get('short_description')
        description = request.form.get('description')
        location = request.form.get('location')
        department = request.form.get('department') or "General"

        # Get GPS coordinates from form (user's current location)
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Convert to float if available, otherwise set to None
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except (ValueError, TypeError):
            latitude = None
            longitude = None

        # If no GPS coordinates from user, try to geocode the text location
        if not latitude or not longitude:
            try:
                geocoded_coords = geocode_with_retry(location)
                if geocoded_coords:
                    latitude, longitude = geocoded_coords
                    print(f"✅ Successfully geocoded '{location}' to coordinates: Lat={latitude}, Lng={longitude}")
                else:
                    print(f"⚠️ Could not geocode location: '{location}'")
            except Exception as e:
                print(f"⚠️ Geocoding error for '{location}': {e}")

        # Validate mandatory fields
        if not title or not description or not location or not department:
            flash(text["all_fields_mandatory"], "danger")
            return redirect(url_for('submit_report'))

        # Handle media uploads (photos and videos)
        media_files = request.files.getlist('media')
        media_filenames = []
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        for media in media_files:
            if media and media.filename:
                # Check file size (20MB max)
                media.seek(0, os.SEEK_END)
                file_size = media.tell()
                media.seek(0)
                if file_size > 20 * 1024 * 1024:  # 20MB
                    flash(text["file_too_large"].format(filename=media.filename), "danger")
                    return redirect(url_for('submit_report'))

                timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
                filename = f"{timestamp}_{secure_filename(media.filename)}"
                media.save(os.path.join(upload_folder, filename))
                media_filenames.append(filename)

        media_str = ';'.join(media_filenames) if media_filenames else None

        # Create report with GPS coordinates
        report = Report(
            title=title,
            short_description=short_description,
            description=description,
            location=location,
            latitude=latitude,
            longitude=longitude,
            department=department,
            media=media_str,
            user_id=session['user_id']
        )
        db.session.add(report)
        db.session.commit()

        # Log GPS coordinates for debugging
        if latitude and longitude:
            print(f"✅ Report submitted with GPS coordinates: Lat={latitude}, Lng={longitude}")
        else:
            print("⚠️ Report submitted without GPS coordinates")

        flash(text["report_submitted_successfully"], "success")
        return redirect(url_for('home'))
    return render_template('submit_report_new.html', text=text)


# ================== RUN ==================
if __name__ == '__main__':
    # Database reset logic for prototype mode
    db_path = 'civic_reports.db'

    # Check if database file exists and delete it
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✅ Old database '{db_path}' deleted successfully!")
        except Exception as e:
            print(f"⚠️  Warning: Could not delete old database: {e}")

    # Create fresh database schema
    with app.app_context():
        db.create_all()
        print("✅ Database reset successfully! Fresh schema created.")

    app.run(debug=True)
