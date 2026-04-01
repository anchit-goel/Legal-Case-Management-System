
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env if present (for local dev)
load_dotenv()


def get_connection():
    """Returns a MySQL connection using DB_* environment variables.

    Production deployment must set: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    For backwards compatibility, MYSQL_* env names are also supported.
    If DB_HOST is not set, this function will return None instead of connecting to localhost.
    """
    try:
        # Prefer DB_* environment variables (required in production)
        DB_HOST = os.environ.get("DB_HOST") or os.environ.get("MYSQLHOST") or os.environ.get("MYSQL_HOST")
        if not DB_HOST:
            print("DB_HOST not set; skipping DB connection (set DB_HOST in your environment)")
            return None

        DB_PORT = int(os.environ.get("DB_PORT") or os.environ.get("MYSQLPORT") or os.environ.get("MYSQL_PORT", 3306))
        DB_USER = os.environ.get("DB_USER") or os.environ.get("MYSQLUSER") or os.environ.get("MYSQL_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD") or os.environ.get("MYSQLPASSWORD") or os.environ.get("MYSQL_PASSWORD")
        DB_NAME = os.environ.get("DB_NAME") or os.environ.get("MYSQLDATABASE") or os.environ.get("MYSQL_DATABASE")

        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                auth_plugin='mysql_native_password',
                connection_timeout=10,
            )
            return connection
        except Error as err:
            # If database does not exist, attempt to create it then reconnect
            if getattr(err, 'errno', None) == 1049 and DB_NAME:
                temp_conn = mysql.connector.connect(
                    host=DB_HOST, port=DB_PORT, user=DB_USER,
                    password=DB_PASSWORD, auth_plugin='mysql_native_password', connection_timeout=10
                )
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
                temp_conn.commit()
                temp_cursor.close()
                temp_conn.close()

                return mysql.connector.connect(
                    host=DB_HOST, port=DB_PORT, user=DB_USER,
                    password=DB_PASSWORD, database=DB_NAME,
                    auth_plugin='mysql_native_password', connection_timeout=10
                )
            else:
                raise err
    except Error as e:
        print(f"MySQL connection failed: {e}")
        return None

def ensure_tables_exist():
    connection = get_connection()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20),
                address TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lawyers (
                lawyer_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                specialization VARCHAR(100)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id INT PRIMARY KEY AUTO_INCREMENT,
                case_number VARCHAR(50) UNIQUE NOT NULL,
                case_type VARCHAR(100),
                status ENUM('Active', 'Closed', 'Pending') DEFAULT 'Active',
                client_id INT,
                lawyer_id INT,
                filing_date DATE,
                description TEXT,
                FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE SET NULL,
                FOREIGN KEY (lawyer_id) REFERENCES lawyers(lawyer_id) ON DELETE SET NULL
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM lawyers")
        result = cursor.fetchone()
        if result and result[0] == 0:
            cursor.execute("INSERT INTO lawyers (name, specialization) VALUES ('Sarah Smith', 'Corporate Law'), ('Michael Johnson', 'Family Law'), ('Patricia Williams', 'Criminal Law')")
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Table initialization failed: {e}")

def test_connection():
    """Verification for DB connectivity during deployment."""
    ensure_tables_exist()
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        connection.close()
        return True, version[0] if version else "Unknown"
    return False, None

if __name__ == "__main__":
    ok, ver = test_connection()
    if ok:
        print(f"Connection OK! MySQL Version: {ver}")
    else:
        print("Connection Failed!")