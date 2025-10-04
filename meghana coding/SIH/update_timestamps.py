from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    # Update existing timestamps from UTC to IST by adding 5 hours 30 minutes
    ist_offset = timedelta(hours=5, minutes=30)
    conn = db.engine.connect()

    # Update 'created_at' in 'report' table
    conn.execute(db.text(
        "UPDATE report SET created_at = datetime(created_at, '+5 hours', '+30 minutes') WHERE created_at IS NOT NULL"
    ))
    # Update 'created_at' in 'update' table
    conn.execute(db.text(
        'UPDATE "update" SET created_at = datetime(created_at, \'+5 hours\', \'+30 minutes\') WHERE created_at IS NOT NULL'
    ))
    # Update 'created_at' in 'feedback' table
    conn.execute(db.text(
        "UPDATE feedback SET created_at = datetime(created_at, '+5 hours', '+30 minutes') WHERE created_at IS NOT NULL"
    ))

    conn.commit()
    print('Timestamps updated to IST successfully!')
