from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civic_reports.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    # Add new column otp_created_at to user table
    with db.engine.connect() as conn:
        try:
            conn.execute(db.text('ALTER TABLE user ADD COLUMN otp_created_at DATETIME;'))
            print('otp_created_at column added successfully!')
        except Exception as e:
            print(f'Error adding otp_created_at column: {e}')
        conn.commit()
