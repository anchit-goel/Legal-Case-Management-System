
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