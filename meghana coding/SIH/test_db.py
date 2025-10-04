from app import app, db, Report

with app.app_context():
    print("Testing database connection...")
    try:
        reports = Report.query.all()
        print(f"Found {len(reports)} reports in database")

        # Test creating a sample report
        sample_report = Report(
            title="Test Report",
            description="This is a test report",
            city="Test City",
            locality="Test Locality",
            street="Test Street",
            address="Test Address"
        )
        db.session.add(sample_report)
        db.session.commit()
        print("Sample report created successfully!")

        # Clean up
        db.session.delete(sample_report)
        db.session.commit()
        print("Sample report deleted successfully!")

    except Exception as e:
        print(f"Error: {e}")
