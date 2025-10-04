from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    # Check if photo column exists in report table
    with db.engine.connect() as conn:
        result = conn.execute(db.text("PRAGMA table_info(report);"))
        columns = [row[1] for row in result.fetchall()]
        if 'photo' not in columns:
            try:
                conn.execute(db.text('ALTER TABLE report ADD COLUMN photo VARCHAR(1000);'))
                print('photo column added successfully!')
            except Exception as e:
                print(f'Error adding photo column: {e}')
        else:
            print('photo column already exists.')
        conn.commit()
