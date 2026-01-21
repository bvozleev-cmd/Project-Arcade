import sqlite3

DB_NAME = "progress.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY,
            completed INTEGER DEFAULT 0,
            crystals INTEGER DEFAULT 0
        )
        """)
        for i in range(1, 6):
            c.execute(
                "INSERT OR IGNORE INTO levels (id) VALUES (?)", (i,)
            )
        conn.commit()


def get_levels():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, completed, crystals FROM levels")
        return c.fetchall()


def get_level(level_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT completed, crystals FROM levels WHERE id=?",
            (level_id,)
        )
        return c.fetchone()


def complete_level(level_id, crystals):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        UPDATE levels
        SET completed = 1,
            crystals = MAX(crystals, ?)
        WHERE id = ?
        """, (crystals, level_id))
        conn.commit()


def update_crystals(level_id, crystals):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        UPDATE levels
        SET crystals = MAX(crystals, ?)
        WHERE id = ?
        """, (crystals, level_id))
        conn.commit()
