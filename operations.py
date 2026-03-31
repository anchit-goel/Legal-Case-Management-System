from db import get_connection


# ---------------- HELPER FUNCTIONS ----------------

def client_exists(email):
    conn = get_connection()
    if conn is None:
        return False
    cursor = conn.cursor()

    query = "SELECT * FROM clients WHERE email=%s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result is not None


# ---------------- CLIENTS ----------------

def add_client(first_name, last_name, email, phone, address):
    conn = get_connection()
    if conn is None:
        raise Exception("Cannot connect to Database (ensure MYSQLHOST is configured)")
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO clients (first_name, last_name, email, phone, address)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (first_name, last_name, email, phone, address))
        conn.commit()
        print("Client added successfully")

    except Exception as e:
        print("Error adding client:", e)
        raise e

    finally:
        cursor.close()
        conn.close()


def get_clients():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT client_id, first_name, last_name, email, phone
        FROM clients
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def update_client(client_id, first_name, last_name, email, phone, address):
    conn = get_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    try:
        query = """
        UPDATE clients
        SET first_name=%s, last_name=%s, email=%s, phone=%s, address=%s
        WHERE client_id=%s
        """
        cursor.execute(query, (first_name, last_name, email, phone, address, client_id))
        conn.commit()
        print("Client updated successfully")

    except Exception as e:
        print("Error updating client:", e)

    finally:
        cursor.close()
        conn.close()


def delete_client(client_id):
    conn = get_connection()
    if conn is None:
        print("Unable to connect to database")
        return
    cursor = conn.cursor()

    try:
        query = "DELETE FROM clients WHERE client_id = %s"
        cursor.execute(query, (client_id,))
        conn.commit()
        print("Client deleted successfully")

    except Exception as e:
        print("Error deleting client:", e)

    finally:
        cursor.close()
        conn.close()


def search_client(name):
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()

    query = """
    SELECT * FROM clients
    WHERE first_name LIKE %s OR last_name LIKE %s
    """
    cursor.execute(query, ('%' + name + '%', '%' + name + '%'))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# ---------------- LAWYERS ----------------

def add_lawyer(name, specialization):
    conn = get_connection()
    if conn is None:
        print("Unable to connect to database")
        return
    cursor = conn.cursor()

    try:
        query = "INSERT INTO lawyers (name, specialization) VALUES (%s, %s)"
        cursor.execute(query, (name, specialization))
        conn.commit()
        print("Lawyer added successfully")

    except Exception as e:
        print("Error adding lawyer:", e)

    finally:
        cursor.close()
        conn.close()


def get_lawyers():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT lawyer_id, name, specialization FROM lawyers")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data if data else []


# ---------------- CASES ----------------

def add_case(case_number, case_type, client_id, lawyer_id, filing_date, description):
    conn = get_connection()
    if conn is None:
        print("Unable to connect to database")
        return
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO cases (case_number, case_type, client_id, lawyer_id, filing_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (case_number, case_type, client_id, lawyer_id, filing_date, description))
        conn.commit()
        print("Case added successfully")

    except Exception as e:
        print("Error adding case:", e)

    finally:
        cursor.close()
        conn.close()


def get_cases():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()

    cursor.execute("""
        SELECT case_id, case_number, case_type, status, client_id
        FROM cases
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def update_case_status(case_id, status):
    conn = get_connection()
    if conn is None:
        print("Unable to connect to database")
        return
    cursor = conn.cursor()

    try:
        query = """
        UPDATE cases
        SET status = %s
        WHERE case_id = %s
        """
        cursor.execute(query, (status, case_id))
        conn.commit()
        print("Case status updated")

    except Exception as e:
        print("Error updating case:", e)

    finally:
        cursor.close()
        conn.close()


def get_case_details():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()

    query = """
    SELECT 
        cases.case_id,
        cases.case_number,
        clients.first_name,
        clients.last_name,
        cases.case_type,
        cases.status
    FROM cases
    JOIN clients ON cases.client_id = clients.client_id
    """

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def get_case_by_id(case_id):
    """Get a specific case by ID with full details"""
    conn = get_connection()
    if conn is None:
        return None
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        c.case_id,
        c.case_number,
        c.case_type,
        c.status,
        c.filing_date,
        c.description,
        CASE 
            WHEN cl.first_name IS NULL THEN 'Unknown Client'
            ELSE CONCAT(cl.first_name, ' ', cl.last_name)
        END AS client_name,
        cl.email AS client_email,
        cl.phone AS client_phone,
        cl.address AS client_address,
        l.name AS lawyer_name,
        l.specialization AS lawyer_specialization
    FROM cases c
    LEFT JOIN clients cl ON c.client_id = cl.client_id
    LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id
    WHERE c.case_id = %s
    """
    cursor.execute(query, (case_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result if result else None


def get_all_cases():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        c.case_id,
        c.status,
        CONCAT(COALESCE(cl.first_name, ''), ' ', COALESCE(cl.last_name, '')) AS client_name,
        COALESCE(l.name, 'Unassigned') AS lawyer_name
    FROM cases c
    LEFT JOIN clients cl ON c.client_id = cl.client_id
    LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id
    ORDER BY c.case_id DESC
    """)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result if result else []


# ---------------- HEARINGS ----------------

def add_hearing(case_id, hearing_date, notes):
    conn = get_connection()
    if conn is None:
        print("Unable to connect to database")
        return
    cursor = conn.cursor()

    try:
        query = """
        INSERT INTO hearings (case_id, hearing_date, notes)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (case_id, hearing_date, notes))
        conn.commit()
        print("Hearing added successfully")

    except Exception as e:
        print("Error adding hearing:", e)

    finally:
        cursor.close()
        conn.close()


def get_hearings():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM hearings")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# ---------------- REPORTS ----------------

def cases_per_lawyer():
    conn = get_connection()
    if conn is None:
        return []
    cursor = conn.cursor()

    query = """
    SELECT lawyers.name, COUNT(cases.case_id)
    FROM cases
    JOIN lawyers ON cases.lawyer_id = lawyers.lawyer_id
    GROUP BY lawyers.name
    """

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data