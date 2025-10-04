import sqlite3

DB_NAME = "reports.db"

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    location TEXT,
    department TEXT,
    status TEXT,
    submitted TEXT,
    photo TEXT
)
""")
conn.commit()
conn.close()

print("Database and tables created successfully!")
