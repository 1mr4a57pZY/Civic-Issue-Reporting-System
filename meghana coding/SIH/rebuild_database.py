#!/usr/bin/env python3
"""
Database rebuild script for Civic Reports Flask application.
This script will:
1. Remove old database files
2. Create new database with correct schema
3. Test the problematic query
"""

import os
import sys
from datetime import datetime
import pytz

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, User, Report, Update, Notification, Feedback

def rebuild_database():
    """Rebuild the database from scratch"""

    print("🔄 Starting database rebuild process...")

    # Step 1: Remove old database files
    db_files = ['civic_reports.db', 'reports.db', 'instance/civic_reports.db']
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Removed old database file: {db_file}")

    # Step 2: Create new database with correct schema
    with app.app_context():
        print("📊 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

        # Step 3: Test the problematic query
        print("🧪 Testing the problematic query...")
        try:
            # Test the query that was failing
            mobile = "1234567890"
            email = "test@example.com"

            # This should work now
            result = User.query.filter((User.mobile == mobile) | (User.email == email)).first()
            print("✅ Query test passed! No errors occurred.")

            if result:
                print(f"   Found user: {result.name} (ID: {result.id})")
            else:
                print("   No user found (expected for empty database)")

        except Exception as e:
            print(f"❌ Query test failed: {e}")
            return False

        # Step 4: Verify all tables exist with correct columns
        print("🔍 Verifying database schema...")
        inspector = db.inspect(db.engine)

        tables = inspector.get_table_names()
        print(f"   Tables found: {tables}")

        # Check User table columns
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        print(f"   User table columns: {user_columns}")

        # Check Report table columns
        report_columns = [col['name'] for col in inspector.get_columns('report')]
        print(f"   Report table columns: {report_columns}")

        # Verify required columns exist
        required_user_columns = ['id', 'name', 'email', 'mobile', 'otp', 'otp_created_at', 'is_verified', 'created_at']
        required_report_columns = ['id', 'title', 'short_description', 'description', 'location', 'latitude', 'longitude', 'status', 'department', 'photo', 'media', 'created_at', 'updated_at', 'user_id']

        user_missing = set(required_user_columns) - set(user_columns)
        report_missing = set(required_report_columns) - set(report_columns)

        if user_missing:
            print(f"❌ Missing User columns: {user_missing}")
            return False
        else:
            print("✅ All required User columns present")

        if report_missing:
            print(f"❌ Missing Report columns: {report_missing}")
            return False
        else:
            print("✅ All required Report columns present")

    print("🎉 Database rebuild completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run your Flask application: python app.py")
    print("2. Test user registration and report submission")
    print("3. Verify that the mobile/email query works in your application")

    return True

if __name__ == "__main__":
    rebuild_database()
