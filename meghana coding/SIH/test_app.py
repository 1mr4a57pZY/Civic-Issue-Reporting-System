from app import app, db, Report

with app.app_context():
    try:
        reports = Report.query.all()
        print(f'Database connected successfully. Found {len(reports)} reports.')
        if reports:
            print('Sample report:', reports[0].title, reports[0].city, reports[0].locality)
    except Exception as e:
        print(f'Error: {e}')
