import datetime
import pytz
from app import app, db, Report, Update, Feedback

def check_existing_reports():
    with app.app_context():
        # Check all reports
        reports = Report.query.all()
        print(f"=== EXISTING REPORTS ({len(reports)} found) ===")

        for report in reports:
            print(f"\nReport ID: {report.id}")
            print(f"Title: {report.title}")
            print(f"Created at (raw): {report.created_at}")
            print(f"Created at (IST): {report.created_at.astimezone(pytz.timezone('Asia/Kolkata'))}")
            print(f"Updated at (raw): {report.updated_at}")
            print(f"Updated at (IST): {report.updated_at.astimezone(pytz.timezone('Asia/Kolkata'))}")

            # Check updates
            for update in report.updates:
                print(f"  Update created_at (raw): {update.created_at}")
                print(f"  Update created_at (IST): {update.created_at.astimezone(pytz.timezone('Asia/Kolkata'))}")

            # Check feedbacks
            for feedback in report.feedbacks:
                print(f"  Feedback created_at (raw): {feedback.created_at}")
                print(f"  Feedback created_at (IST): {feedback.created_at.astimezone(pytz.timezone('Asia/Kolkata'))}")

if __name__ == "__main__":
    check_existing_reports()
