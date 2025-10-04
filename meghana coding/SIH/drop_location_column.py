from app import app, db
from sqlalchemy import text

with app.app_context():
    # Drop the location column if it exists
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE report DROP COLUMN location'))
            conn.commit()
        print("Location column dropped successfully!")
    except Exception as e:
        print(f"Error dropping location column: {e}")

    # Verify the current schema
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(report)"))
            columns = result.fetchall()
        print("Current report table columns:")
        for col in columns:
            print(f"- {col[1]}: {col[2]} {'NOT NULL' if col[3] else 'NULL'}")
    except Exception as e:
        print(f"Error checking schema: {e}")
