import os
import sqlite3

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


_db_initialized = False


class SQLiteCursorWrapper:
    def __init__(self, cursor, dictionary=False):
        self._cursor = cursor
        self._dictionary = dictionary

    def execute(self, query, params=None):
        normalized = query.replace("%s", "?")
        if params is None:
            self._cursor.execute(normalized)
        else:
            self._cursor.execute(normalized, params)

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        return dict(row) if self._dictionary else tuple(row)

    def fetchall(self):
        rows = self._cursor.fetchall()
        if self._dictionary:
            return [dict(row) for row in rows]
        return [tuple(row) for row in rows]

    def close(self):
        self._cursor.close()


class SQLiteConnectionWrapper:
    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")

    def cursor(self, dictionary=False):
        return SQLiteCursorWrapper(self._conn.cursor(), dictionary=dictionary)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def _sqlite_path():
    return os.environ.get("SQLITE_PATH", "legal_local.db")


def ensure_tables_exist(force=False):
    global _db_initialized
    if _db_initialized and not force:
        return

    db_path = _sqlite_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    with conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                address TEXT,
                password TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS lawyers (
                lawyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialization TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                case_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT UNIQUE NOT NULL,
                case_type TEXT,
                status TEXT DEFAULT 'Active',
                client_id INTEGER,
                lawyer_id INTEGER,
                filing_date TEXT,
                description TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE SET NULL,
                FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id) ON DELETE SET NULL
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS hearings (
                hearing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                hearing_date TEXT,
                notes TEXT,
                FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (datetime('now')),
                user_role TEXT,
                user_id INTEGER,
                action TEXT,
                entity TEXT,
                entity_id INTEGER,
                details TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS case_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                changed_at TEXT DEFAULT (datetime('now')),
                changed_by_role TEXT,
                changed_by_id INTEGER,
                field_name TEXT,
                old_value TEXT,
                new_value TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token TEXT PRIMARY KEY,
                user_role TEXT,
                user_email TEXT,
                expires_at TEXT,
                used INTEGER DEFAULT 0
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS case_feedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                author_role TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                rating INTEGER,
                feedback_text TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS date_change_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER NOT NULL,
                requested_by_role TEXT NOT NULL,
                requested_by_id INTEGER NOT NULL,
                current_date TEXT,
                requested_date TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'Pending',
                court_note TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                resolved_at TEXT,
                FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipient_role TEXT NOT NULL,
                recipient_id INTEGER,
                case_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            )
            """
        )

        # Backward-compatible migration for older DBs missing columns
        def has_column(table, column):
            cur.execute(f"PRAGMA table_info({table})")
            return column in [r[1] for r in cur.fetchall()]

        if not has_column("clients", "password"):
            cur.execute("ALTER TABLE clients ADD COLUMN password TEXT")
        if not has_column("lawyers", "email"):
            cur.execute("ALTER TABLE lawyers ADD COLUMN email TEXT")
        if not has_column("lawyers", "password"):
            cur.execute("ALTER TABLE lawyers ADD COLUMN password TEXT")

    conn.close()
    _db_initialized = True


def get_connection():
    ensure_tables_exist()
    return SQLiteConnectionWrapper(_sqlite_path())


def test_connection():
    try:
        ensure_tables_exist()
        connection = SQLiteConnectionWrapper(_sqlite_path())
        cursor = connection.cursor()
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()
        cursor.close()
        connection.close()
        return True, version[0] if version else "Unknown"
    except Exception:
        return False, None


if __name__ == "__main__":
    ok, ver = test_connection()
    if ok:
        print(f"Connection OK! SQLite Version: {ver}")
    else:
        print("Connection Failed!")
