import pytest
from full_flask_app.app import app, db, User, Report
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_and_otp_flow(client):
    # Register user
    response = client.post('/register', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'mobile': ''
    }, follow_redirects=True)
    assert b'Your OTP is' in response.data or response.status_code == 200

    # Get user from DB
    user = User.query.filter_by(email='testuser@example.com').first()
    assert user is not None
    otp = user.otp

    # Verify OTP
    response = client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)
    assert b'OTP verified successfully' in response.data

def test_submit_report_requires_login(client):
    response = client.get('/submit', follow_redirects=True)
    assert b'You must log in first' in response.data

def test_submit_report(client):
    # Register and verify user first
    client.post('/register', data={
        'name': 'Reporter',
        'email': 'reporter@example.com',
        'mobile': ''
    }, follow_redirects=True)
    user = User.query.filter_by(email='reporter@example.com').first()
    otp = user.otp
    client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)

    # Submit report
    response = client.post('/submit', data={
        'title': 'Test Issue',
        'description': 'Description of issue',
        'location': 'Test Location',
        'department': 'General'
    }, follow_redirects=True)
    assert b'Report submitted successfully' in response.data

def test_admin_update_report_status(client):
    # Setup user and report
    client.post('/register', data={
        'name': 'AdminUser',
        'email': 'adminuser@example.com',
        'mobile': ''
    }, follow_redirects=True)
    user = User.query.filter_by(email='adminuser@example.com').first()
    otp = user.otp
    client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)

    # Submit report
    client.post('/submit', data={
        'title': 'Admin Test Issue',
        'description': 'Admin description',
        'location': 'Admin Location',
        'department': 'General'
    }, follow_redirects=True)
    report = Report.query.filter_by(title='Admin Test Issue').first()
    assert report is not None

    # Update report status to resolved
    response = client.post(f'/admin/report/{report.id}', data={
        'status': 'resolved',
        'comment': 'Issue fixed',
        'photo': []
    }, follow_redirects=True)
    assert b'Report updated successfully' in response.data

def test_email_notification_sent(monkeypatch, client):
    sent_emails = []

    def fake_send(msg):
        sent_emails.append(msg)

    monkeypatch.setattr('full_flask_app.app.mail.send', fake_send)

    # Register and verify user
    client.post('/register', data={
        'name': 'NotifyUser',
        'email': 'notifyuser@example.com',
        'mobile': ''
    }, follow_redirects=True)
    user = User.query.filter_by(email='notifyuser@example.com').first()
    otp = user.otp
    client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)

    # Submit report
    client.post('/submit', data={
        'title': 'Notify Issue',
        'description': 'Notify description',
        'location': 'Notify Location',
        'department': 'General'
    }, follow_redirects=True)
    report = Report.query.filter_by(title='Notify Issue').first()

    # Update report status to resolved to trigger email
    client.post(f'/admin/report/{report.id}', data={
        'status': 'resolved',
        'comment': 'Fixed',
        'photo': []
    }, follow_redirects=True)

    assert len(sent_emails) > 0
    assert any('Your reported issue has been resolved' in email.subject for email in sent_emails)
