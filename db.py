
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()


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


def ensure_tables_exist():
    connection = SQLiteConnectionWrapper(_sqlite_path())
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lawyers (
            lawyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT
        )
        """
    )
    cursor.execute(
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
    cursor.execute(
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

    cursor.execute("SELECT COUNT(*) FROM lawyers")
    row = cursor.fetchone()
    if row and row[0] == 0:
        cursor.execute(
            "INSERT INTO lawyers (name, specialization) VALUES (?, ?), (?, ?), (?, ?)",
            ("Sarah Smith", "Corporate Law", "Michael Johnson", "Family Law", "Patricia Williams", "Criminal Law")
        )

    connection.commit()
    cursor.close()
    connection.close()


def get_connection():
    ensure_tables_exist()
    return SQLiteConnectionWrapper(_sqlite_path())


def test_connection():
    try:
        ensure_tables_exist()
        connection = get_connection()
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