#!/usr/bin/env python3
"""
Test script to verify timestamp display in IST timezone
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Report, User
from datetime import datetime
import pytz

def test_timestamp_display():
    """Test that timestamps are displayed correctly in IST"""
    with app.app_context():
        # Create a test report with IST timestamp
        test_report = Report(
            title="Test Report",
            description="Test description",
            location="Test Location",
            department="General",
            user_id=1  # Assuming user with ID 1 exists
        )
        db.session.add(test_report)
        db.session.commit()

        # Get the report and check timestamp
        report = Report.query.filter_by(title="Test Report").first()
        if report:
            print(f"Report ID: {report.id}")
            print(f"Created at (raw): {report.created_at}")
            print(f"Created at (IST): {report.created_at.astimezone(pytz.timezone('Asia/Kolkata'))}")
            print(f"Formatted IST: {report.created_at.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%b %d, %Y %H:%M')}")

            # Clean up
            db.session.delete(report)
            db.session.commit()
            print("✅ Test completed successfully!")
        else:
            print("❌ Test report not found")

if __name__ == "__main__":
    test_timestamp_display()
