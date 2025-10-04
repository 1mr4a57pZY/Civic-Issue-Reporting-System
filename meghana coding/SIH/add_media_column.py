from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    # Check if media column exists in report table
    with db.engine.connect() as conn:
        result = conn.execute(db.text("PRAGMA table_info(report);"))
        columns = [row[1] for row in result.fetchall()]
        if 'media' not in columns:
            try:
                conn.execute(db.text('ALTER TABLE report ADD COLUMN media VARCHAR(2000);'))
                print('media column added successfully!')
            except Exception as e:
                print(f'Error adding media column: {e}')
        else:
            print('media column already exists.')
        conn.commit()
