
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env if present (for local dev)
load_dotenv()

def get_connection():
    """Returns a MySQL connection using either MYSQL_URL or individual components."""
    try:
        # Standardize for Railway environment names (MYSQLHOST, MYSQLPORT, etc.)
        MYSQL_HOST = os.environ.get("MYSQLHOST", os.environ.get("MYSQL_HOST", "localhost"))
        MYSQL_PORT = int(os.environ.get("MYSQLPORT", os.environ.get("MYSQL_PORT", 3306)))
        MYSQL_USER = os.environ.get("MYSQLUSER", os.environ.get("MYSQL_USER", "root"))
        MYSQL_PASSWORD = os.environ.get("MYSQLPASSWORD", os.environ.get("MYSQL_PASSWORD", ""))
        MYSQL_DB = os.environ.get("MYSQLDATABASE", os.environ.get("MYSQL_DATABASE", "legal_db"))
        
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            # Cloud auth plugin support
            auth_plugin='mysql_native_password',
            connection_timeout=10
        )
        return connection
    except Error as e:
        print(f"MySQL connection failed: {e}")
        return None

def test_connection():
    """Verification for DB connectivity during deployment."""
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