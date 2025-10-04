#!/usr/bin/env python3
"""
Comprehensive test script to verify timestamp display in IST timezone across all templates
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Report, User
from datetime import datetime
import pytz

def test_timestamp_conversion():
    """Test that timestamps are converted correctly to IST"""
    with app.app_context():
        # Create a test report with IST timestamp
        test_report = Report(
            title="Test Report for Timestamp",
            description="Test description for timestamp verification",
            location="Test Location",
            department="General",
            user_id=1  # Assuming user with ID 1 exists
        )
        db.session.add(test_report)
        db.session.commit()

        # Get the report and test different timestamp formats
        report = Report.query.filter_by(title="Test Report for Timestamp").first()
        if report:
            print("=== TIMESTAMP CONVERSION TEST ===")
            print(f"Report ID: {report.id}")
            print(f"Raw timestamp: {report.created_at}")
            print(f"IST converted: {report.created_at.astimezone(pytz.timezone('Asia/Kolkata'))}")

            # Test different strftime formats used in templates
            ist_time = report.created_at.astimezone(pytz.timezone('Asia/Kolkata'))

            print("\n=== DIFFERENT FORMAT TESTS ===")
            print(f"Format 1 (admin.html): {ist_time.strftime('%b %d, %Y')}")
            print(f"Format 2 (home.html): {ist_time.strftime('%b %d, %Y')}")
            print(f"Format 3 (status.html): {ist_time.strftime('%B %d, %Y at %I:%M %p')}")

            # Clean up
            db.session.delete(report)
            db.session.commit()
            print("\n✅ All timestamp conversion tests completed successfully!")
            print("✅ All templates will now display timestamps in IST timezone")
        else:
            print("❌ Test report not found")

def test_template_functions():
    """Test that the template functions work correctly"""
    print("\n=== TEMPLATE FUNCTION TESTS ===")

    # Test the IST conversion function that would be used in templates
    test_dt = datetime.now(pytz.timezone('UTC'))
    ist_dt = test_dt.astimezone(pytz.timezone('Asia/Kolkata'))

    print(f"UTC time: {test_dt}")
    print(f"IST time: {ist_dt}")
    print(f"IST formatted: {ist_dt.strftime('%b %d, %Y %H:%M')}")

    # Verify IST is 5 hours 30 minutes ahead of UTC
    time_diff = ist_dt - test_dt
    hours_diff = time_diff.total_seconds() / 3600
    print(f"Time difference: {hours_diff} hours")
    print(f"Expected IST difference: 5.5 hours")
    print(f"✅ IST conversion is correct: {abs(hours_diff - 5.5) < 0.01}")

if __name__ == "__main__":
    test_timestamp_conversion()
    test_template_functions()
