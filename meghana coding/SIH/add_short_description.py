from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    # Check if short_description column exists in report table
    with db.engine.connect() as conn:
        result = conn.execute(db.text("PRAGMA table_info(report);"))
        columns = [row[1] for row in result.fetchall()]
        if 'short_description' not in columns:
            try:
                conn.execute(db.text('ALTER TABLE report ADD COLUMN short_description VARCHAR(300);'))
                print('short_description column added successfully!')
            except Exception as e:
                print(f'Error adding short_description column: {e}')
        else:
            print('short_description column already exists.')
        conn.commit()
