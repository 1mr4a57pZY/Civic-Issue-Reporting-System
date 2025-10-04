# Civic Issue Reporting System

A comprehensive web application built with Flask that enables citizens to report civic issues such as potholes, garbage problems, street light failures, and more. The system includes user authentication, admin management, real-time notifications, and multilingual support.

## 🚀 Features

### User Features
- **User Registration & Authentication**: Secure registration with OTP verification via email or mobile
- **Report Submission**: Submit detailed civic issue reports with:
  - Title and detailed descriptions
  - Location with automatic GPS geocoding
  - Department selection (Public Works, Sanitation, Electricity, etc.)
  - Media uploads (photos and videos up to 20MB)
- **Dashboard**: View all submitted reports with status tracking
- **Notifications**: Real-time notifications for report updates
- **Feedback System**: Rate and provide feedback on resolved issues
- **Multilingual Support**: Available in English, Hindi, and Telugu

### Admin Features
- **Admin Dashboard**: Comprehensive overview of all reports
- **Report Management**: Update report status (Pending → In Progress → Resolved)
- **Progress Tracking**: Add comments and upload progress photos
- **User Communication**: Automatic email notifications for resolved issues
- **Analytics**: View report statistics and department-wise breakdowns

### Technical Features
- **GPS Integration**: Automatic location geocoding using external APIs
- **Media Management**: Secure file upload system with size validation
- **Database Migrations**: Version-controlled database schema management
- **Email Integration**: SMTP-based email notifications
- **Responsive Design**: Mobile-friendly web interface
- **Time Zone Support**: IST (Indian Standard Time) timestamps

## 🛠️ Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Migrate**: Database migration management
- **Flask-Mail**: Email functionality
- **Flask-Babel**: Internationalization and localization

### Database
- **SQLite**: Lightweight database (easily configurable for PostgreSQL/MySQL)

### Frontend
- **HTML5/CSS3**: Responsive web interface
- **JavaScript**: Client-side interactions
- **Bootstrap**: UI framework (via custom CSS)

### External Services
- **Geocoding API**: Location coordinate conversion
- **SMTP**: Email delivery

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Git
- SMTP email account (Gmail recommended)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1mr4a57pZY/Civic-Issue-Reporting-System.git
   cd Civic-Issue-Reporting-System
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # OR using pyproject.toml
   pip install -e .
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

## ⚙️ Setup and Configuration

1. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. **Configure email settings:**
   - Update `app.config['MAIL_USERNAME']` and `app.config['MAIL_PASSWORD']` in `app.py`
   - For Gmail, use an App Password instead of your regular password

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## 📖 Usage

### For Citizens
1. **Register**: Create an account with email or mobile number
2. **Verify**: Enter the OTP sent to your email/mobile
3. **Submit Report**: Fill in the issue details, location, and upload media
4. **Track Progress**: Monitor your reports on the dashboard
5. **Provide Feedback**: Rate resolved issues

### For Administrators
1. **Access Admin Panel**: Navigate to `/admin`
2. **Review Reports**: View all submitted reports
3. **Update Status**: Change report status and add comments/photos
4. **Monitor Analytics**: Track system usage and resolution rates

## 🗄️ Database Schema

### User Model
- `id`: Primary key
- `name`: User's full name
- `email`: Email address (optional)
- `mobile`: Mobile number (optional)
- `otp`: Temporary OTP storage
- `otp_created_at`: OTP timestamp
- `is_verified`: Account verification status
- `created_at`: Account creation timestamp

### Report Model
- `id`: Primary key
- `title`: Issue title
- `short_description`: Brief summary
- `description`: Detailed issue description
- `location`: Text location
- `latitude/longitude`: GPS coordinates
- `status`: Current status (pending/in_progress/resolved)
- `department`: Assigned department
- `media`: Uploaded file paths
- `created_at/updated_at`: Timestamps
- `user_id`: Foreign key to User

### Update Model
- `id`: Primary key
- `report_id`: Foreign key to Report
- `status`: Status update
- `comment`: Admin comments
- `photo`: Progress photo paths
- `created_at`: Update timestamp

### Notification Model
- `id`: Primary key
- `user_id`: Foreign key to User
- `message`: Notification text
- `is_read`: Read status
- `created_at`: Notification timestamp

### Feedback Model
- `id`: Primary key
- `report_id`: Foreign key to Report
- `rating`: User rating (1-5)
- `comment`: Feedback text
- `created_at`: Feedback timestamp

## 🔌 API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET /send_otp` - Send OTP for verification
- `GET/POST /verify_otp` - Verify OTP and login
- `GET /logout` - User logout

### Reports
- `GET /` - Home page
- `GET/POST /submit` - Submit new report
- `GET /admin` - Admin dashboard
- `GET/POST /admin/report/<id>` - Admin report details
- `POST /submit_feedback/<id>` - Submit user feedback

### Utilities
- `POST /set_language` - Change language

## 🌍 Multilingual Support

The application supports three languages:
- **English** (default)
- **Hindi** (hi)
- **Telugu** (te)

Language switching is available in the navigation menu.

## 📁 Project Structure

```
civic-issue-reporting-system/
├── app.py                      # Main application file
├── models.py                   # Database models
├── utils.py                    # Utility functions
├── geocoding.py               # Geocoding functionality
├── babel.cfg                  # Babel configuration
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── instance/
│   └── civic_reports.db       # SQLite database
├── migrations/                # Database migrations
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   └── uploads/               # User uploaded files
├── templates/                 # HTML templates
│   ├── home.html
│   ├── register.html
│   ├── submit_report.html
│   ├── admin.html
│   └── ...
├── translations/              # Translation files
│   ├── hi/
│   └── te/
└── README.md                  # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write descriptive commit messages
- Test your changes thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support or questions, please open an issue on GitHub or contact the development team.

## 🙏 Acknowledgments

- Flask framework for the robust web development platform
- OpenStreetMap/Nominatim for geocoding services
- Bootstrap for responsive design components
- The open-source community for various libraries and tools

---

**Made with ❤️ for better civic engagement**
