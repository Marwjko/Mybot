import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS reports(
id INTEGER PRIMARY KEY AUTOINCREMENT,
leave_id TEXT,
name TEXT,
national_id TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

def save_report(d):
    cur.execute(
        "INSERT INTO reports (leave_id,name,national_id) VALUES (?,?,?)",
        (d["leave_id"], d["name"], d["national_id"])
    )
    conn.commit()

def next_leave_id():
    cur.execute("SELECT COUNT(*) FROM reports")
    n = cur.fetchone()[0] + 1
    return f"SL-2026-{n:05d}"
