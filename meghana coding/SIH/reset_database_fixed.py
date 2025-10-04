#!/usr/bin/env python3
"""
Database Reset Script for Civic Reports Flask Application

This script will:
1. Safely delete the current database files (civic_reports.db and reports.db)
2. Recreate all tables using SQLAlchemy models from models.py
3. Verify the database reset was successful
4. Ensure proper Flask application context

Usage: python reset_database_fixed.py
"""

import os
import sys
from datetime import datetime
import pytz

# Add current directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app and models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Report, Update, Notification, Feedback

def create_app():
    """Create and configure the Flask app for database operations"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your_secret_key_here'

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    return app

def reset_database():
    """Reset the database to a fresh state"""

    print("🔄 Starting database reset process...")
    print(f"📅 Reset initiated at: {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')}")

    # Step 1: Identify and remove old database files
    db_files = [
        'civic_reports.db',           # Main database file
        'reports.db',                 # Alternative name mentioned by user
        'instance/civic_reports.db',  # Instance directory version
        'instance/reports.db'         # Instance directory alternative
    ]

    deleted_files = []
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                deleted_files.append(db_file)
                print(f"✅ Deleted database file: {db_file}")
            except Exception as e:
                print(f"⚠️  Warning: Could not delete {db_file}: {e}")

    if not deleted_files:
        print("ℹ️  No existing database files found to delete")
    else:
        print(f"✅ Successfully deleted {len(deleted_files)} database file(s)")

    # Step 2: Create fresh database with correct schema
    app = create_app()

    with app.app_context():
        print("📊 Creating database tables...")

        try:
            # Create all tables defined in models.py
            db.create_all()
            print("✅ Database tables created successfully!")

            # Step 3: Verify the database schema
            print("🔍 Verifying database schema...")

            # Get database inspector
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"   Tables created: {tables}")

            # Verify each table has the expected columns
            expected_tables = ['user', 'report', 'update', 'notification', 'feedback']

            for table_name in expected_tables:
                if table_name in tables:
                    columns = [col['name'] for col in inspector.get_columns(table_name)]
                    print(f"   ✅ {table_name} table: {len(columns)} columns - {columns}")
                else:
                    print(f"   ❌ Missing table: {table_name}")
                    return False

            # Step 4: Test basic database operations
            print("🧪 Testing basic database operations...")

            # Test 1: Create a test user
            test_user = User(
                name="Test User",
                email="test@example.com",
                mobile="1234567890",
                is_verified=True
            )
            db.session.add(test_user)
            db.session.commit()
            print("   ✅ Test user created successfully")

            # Test 2: Create a test report
            test_report = Report(
                title="Test Report",
                description="This is a test report for database verification",
                location="Test Location",
                department="General",
                user_id=test_user.id
            )
            db.session.add(test_report)
            db.session.commit()
            print("   ✅ Test report created successfully")

            # Test 3: Query operations
            user_count = User.query.count()
            report_count = Report.query.count()
            print(f"   ✅ Database contains: {user_count} users, {report_count} reports")

            # Clean up test data
            db.session.delete(test_report)
            db.session.delete(test_user)
            db.session.commit()
            print("   ✅ Test data cleaned up")

            print("✅ All database operations working correctly!")

        except Exception as e:
            print(f"❌ Error during database creation: {e}")
            return False

    print("🎉 Database reset completed successfully!")
    print("\n📋 Summary:")
    print(f"   • Deleted {len(deleted_files)} old database file(s)")
    print("   • Created fresh database with all tables")
    print("   • Verified schema and tested operations")
    print("   • Ready for new report submissions")
    print("\n📋 Next steps:")
    print("1. Run your Flask application: python app.py")
    print("2. Register a new user and submit test reports")
    print("3. Verify that reports are organized properly in the admin dashboard")

    return True

def main():
    """Main function to run the database reset"""
    try:
        success = reset_database()
        if success:
            print("\n✨ Database reset completed successfully! Your application is ready for fresh report submissions.")
            return 0
        else:
            print("\n❌ Database reset failed. Please check the error messages above.")
            return 1
    except KeyboardInterrupt:
        print("\n⚠️  Database reset interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
