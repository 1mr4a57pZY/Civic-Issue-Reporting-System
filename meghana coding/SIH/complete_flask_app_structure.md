# Complete Flask App Structure and Overview

This document outlines the complete Flask app structure including key files, templates, models, and static assets, along with explanations for each section.

---

## 1. app.py

- Main Flask application entry point.
- Configures Flask, SQLAlchemy, Flask-Mail.
- Defines models: User, Report, Update, Feedback, Notification.
- Implements routes for:
  - User registration, OTP verification, login/logout.
  - Language switching.
  - User dashboard and report submission.
  - Admin dashboard and report management.
  - Notifications and feedback.
- Handles email sending for OTP and issue resolution notifications.
- Uses sessions for user authentication and language preference.

---

## 2. Templates (Jinja2)

- `home.html`: User dashboard showing submitted reports and notifications.
- `register.html`: User registration form with email/mobile input.
- `onetimepassword.html`: OTP input form for verification.
- `submit_report.html`: Form for users to submit new civic issues.
- `admin.html`: Admin dashboard listing all reports.
- `admin_report_detail.html`: Admin page to update report status, add comments/photos.
- `status.html`: User view for detailed report status and feedback submission.
- `language_switcher.html`: Dropdown for language selection.
- Other shared partials as needed.

---

## 3. Static Assets

- CSS files (e.g., `premium.css`) for styling.
- JS files for client-side interactivity (file uploads, form validation).
- `static/uploads/` folder for storing uploaded photos with timestamped filenames.

---

## 4. Database Models

- **User**: id, name, email, mobile, otp, otp_created_at, is_verified.
- **Report**: id, title, description, location, status, department, photo(s), created_at, user_id.
- **Update**: id, report_id, status, comment, photo(s), created_at.
- **Feedback**: id, report_id, rating, comment, created_at.
- **Notification**: id, user_id, report_id, message, created_at, is_read.

---

## 5. Email Integration

- Uses Gmail SMTP with app password.
- Sends OTP emails on registration.
- Sends notification emails when issues are resolved.

---

## 6. Additional Features

- Multi-language support with session-based language preference.
- Server-side validation for required fields.
- Flash messages for user feedback.
- Timezone-aware timestamps (Asia/Kolkata).
- Admin can update report status and add updates.
- Users can provide feedback after resolution.

---

## Next Steps

- Generate full code files for `app.py`, templates, and static assets.
- Include detailed comments and instructions for setup and running.
- Provide testing instructions and sample data.

Please confirm to proceed with generating the full codebase files.
