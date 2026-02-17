import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "monitor.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS barangays (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS youth (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barangay_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                age INTEGER,
                gender TEXT,
                program TEXT,
                date_enrolled TEXT,
                notes TEXT,
                FOREIGN KEY(barangay_id) REFERENCES barangays(id) ON DELETE CASCADE
            )
            """
        )

        # Safe migration: add email column if missing
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(youth)").fetchall()]
        if "email" not in cols:
            conn.execute("ALTER TABLE youth ADD COLUMN email TEXT")


def add_barangay(name: str) -> int:
    with get_conn() as conn:
        cur = conn.execute("INSERT OR IGNORE INTO barangays(name) VALUES(?)", (name,))
        if cur.lastrowid:
            return cur.lastrowid
        row = conn.execute("SELECT id FROM barangays WHERE name = ?", (name,)).fetchone()
        return row["id"]


def list_barangays():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name FROM barangays ORDER BY name").fetchall()
        return [dict(r) for r in rows]


def add_youth_record(barangay_id: int, name: str, email: str = None, age: int = None, gender: str = None, program: str = None, date_enrolled: str = None, notes: str = None) -> int:
    if date_enrolled is None:
        date_enrolled = datetime.utcnow().date().isoformat()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO youth (barangay_id, name, email, age, gender, program, date_enrolled, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (barangay_id, name, email, age, gender, program, date_enrolled, notes),
        )
        return cur.lastrowid


def list_youth(barangay_id: int = None):
    with get_conn() as conn:
        if barangay_id:
            rows = conn.execute(
                "SELECT y.*, b.name as barangay FROM youth y JOIN barangays b ON y.barangay_id=b.id WHERE barangay_id = ? ORDER BY y.id",
                (barangay_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT y.*, b.name as barangay FROM youth y JOIN barangays b ON y.barangay_id=b.id ORDER BY y.id"
            ).fetchall()
        return [dict(r) for r in rows]


def update_youth(youth_id: int, **fields):
    if not fields:
        return
    cols = ", ".join(f"{k} = ?" for k in fields.keys())
    vals = list(fields.values()) + [youth_id]
    with get_conn() as conn:
        conn.execute(f"UPDATE youth SET {cols} WHERE id = ?", vals)


def delete_youth(youth_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM youth WHERE id = ?", (youth_id,))


def seed_sample():
    manolo = add_barangay("Poblacion")
    add_barangay("San Isidro")
    add_youth_record(manolo, "Juan Dela Cruz", "juan@example.com", 17, "Male", "Skills Training", None, "Excellent participant")
