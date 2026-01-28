import sqlite3
import os
import sys


def get_save_dir():
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
    else:
        base = os.path.expanduser("~")
    save_dir = os.path.join(base, "CoinQuest")
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


DB_NAME = os.path.join(get_save_dir(), "progress.db")


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        # создаем таблицу уровней
        c.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY,
            completed INTEGER DEFAULT 0,
            crystals INTEGER DEFAULT 0
        )
        """)
        # добавляем уровни
        for i in range(1, 4):  # теперь 4 уровня
            c.execute(
                "INSERT OR IGNORE INTO levels (id) VALUES (?)", (i,)
            )
        conn.commit()

        # Проверяем, есть ли колонка best_time, если нет — добавляем
        c.execute("PRAGMA table_info(levels)")
        columns = [col[1] for col in c.fetchall()]
        if "best_time" not in columns:
            c.execute("ALTER TABLE levels ADD COLUMN best_time REAL")
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


def get_level_crystals(level_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT crystals FROM levels WHERE id=?",
            (level_id,)
        )
        result = c.fetchone()
        return result[0] if result else 0


def init_skins():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS skins (
            id INTEGER PRIMARY KEY,
            name TEXT,
            cost INTEGER,
            unlocked INTEGER DEFAULT 0
        )
        """)
        skins = [
            (1, "character_1", 0),
            (2, "character_2", 10),
            (3, "character_3", 20),
            (4, "character_4", 30),
        ]
        for s in skins:
            c.execute("INSERT OR IGNORE INTO skins (id, name, cost) VALUES (?, ?, ?)", s)
        c.execute("""
        CREATE TABLE IF NOT EXISTS player_skin (
            selected_skin TEXT
        )
        """)
        c.execute("INSERT OR IGNORE INTO player_skin (selected_skin) VALUES ('character_1')")
        conn.commit()


def get_skins():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, cost, unlocked FROM skins")
        return c.fetchall()


def unlock_skin(skin_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE skins SET unlocked=1 WHERE name=?", (skin_name,))
        conn.commit()


def get_selected_skin():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT selected_skin FROM player_skin")
        return c.fetchone()[0]


def select_skin(skin_name):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE player_skin SET selected_skin=?", (skin_name,))
        conn.commit()


def get_level_time(level_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT best_time FROM levels WHERE id=?", (level_id,))
        result = c.fetchone()
        return result[0] if result else None


def update_level_time(level_id, time_seconds):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE levels SET best_time = ? WHERE id=?", (time_seconds, level_id))
        conn.commit()
