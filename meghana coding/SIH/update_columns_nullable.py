from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        with db.engine.connect() as conn:
            # Make the new location columns NOT NULL
            conn.execute(text('ALTER TABLE report ALTER COLUMN city TEXT NOT NULL'))
            conn.execute(text('ALTER TABLE report ALTER COLUMN locality TEXT NOT NULL'))
            conn.execute(text('ALTER TABLE report ALTER COLUMN street TEXT NOT NULL'))
            conn.execute(text('ALTER TABLE report ALTER COLUMN address TEXT NOT NULL'))
            conn.commit()
        print("Columns updated to NOT NULL successfully!")
    except Exception as e:
        print(f"Error updating columns: {e}")

    # Verify the current schema
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(report)"))
            columns = result.fetchall()
        print("Updated report table columns:")
        for col in columns:
            print(f"- {col[1]}: {col[2]} {'NOT NULL' if col[3] else 'NULL'}")
    except Exception as e:
        print(f"Error checking schema: {e}")
