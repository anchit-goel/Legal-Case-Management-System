import hashlib
import json

from db import get_connection


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def log_action(user_role, user_id, action, entity, entity_id, details):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO audit_log (user_role, user_id, action, entity, entity_id, details) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_role, user_id, action, entity, entity_id, json.dumps(details or {})),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_audit_logs(limit=200, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM audit_log ORDER BY log_id DESC LIMIT %s OFFSET %s", (limit, offset))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_user_id_by_email(role, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if role == "lawyer":
            cursor.execute("SELECT lawyer_id FROM lawyers WHERE email=%s", (email,))
        elif role == "client":
            cursor.execute("SELECT client_id FROM clients WHERE email=%s", (email,))
        else:
            return None
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        cursor.close()
        conn.close()


def authenticate_user(role, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if role == "client":
            cursor.execute("SELECT password FROM clients WHERE email=%s", (email,))
        elif role == "lawyer":
            cursor.execute("SELECT password FROM lawyers WHERE email=%s", (email,))
        else:
            return False

        row = cursor.fetchone()
        if not row or not row[0]:
            return False
        return row[0] == _hash_password(password)
    finally:
        cursor.close()
        conn.close()


def client_exists(email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM clients WHERE email=%s", (email,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()


def register_client(first_name, last_name, email, phone, address, password):
    if client_exists(email):
        raise RuntimeError("Client with this email already exists")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clients (first_name, last_name, email, phone, address, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (first_name, last_name, email, phone, address, _hash_password(password)),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def register_lawyer(name, specialization, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO lawyers (name, specialization, email, password) VALUES (%s, %s, %s, %s)",
            (name, specialization, email, _hash_password(password)),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_client(first_name, last_name, email, phone, address):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clients (first_name, last_name, email, phone, address) VALUES (%s, %s, %s, %s, %s)",
            (first_name, last_name, email, phone, address),
        )
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_clients(limit=None, offset=0, search=""):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            query = (
                "SELECT client_id, first_name, last_name, email, phone, address FROM clients "
                "WHERE client_id = %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s "
                "ORDER BY client_id DESC"
            )
            params = (search_id, f"%{search}%", f"%{search}%", f"%{search}%")
        else:
            query = "SELECT client_id, first_name, last_name, email, phone, address FROM clients ORDER BY client_id DESC"
            params = ()

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params = params + (limit, offset)

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def count_clients(search=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            cursor.execute(
                "SELECT COUNT(*) FROM clients WHERE client_id = %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s",
                (search_id, f"%{search}%", f"%{search}%", f"%{search}%"),
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM clients")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def get_client_by_id(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT client_id, first_name, last_name, email, phone, address FROM clients WHERE client_id=%s", (client_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def update_client(client_id, first_name, last_name, email, phone, address):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE clients SET first_name=%s, last_name=%s, email=%s, phone=%s, address=%s WHERE client_id=%s",
            (first_name, last_name, email, phone, address, client_id),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_client(client_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM cases WHERE client_id=%s", (client_id,))
        linked = cursor.fetchone()[0]
        if linked > 0:
            raise RuntimeError(f"Cannot delete client with {linked} active case(s). Reassign or close cases first.")

        cursor.execute("DELETE FROM clients WHERE client_id=%s", (client_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def add_lawyer(name, specialization):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO lawyers (name, specialization) VALUES (%s, %s)", (name, specialization))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_lawyers(limit=None, offset=0, search=""):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            query = "SELECT lawyer_id, name, specialization, email FROM lawyers WHERE lawyer_id = %s OR name LIKE %s OR specialization LIKE %s OR email LIKE %s ORDER BY lawyer_id DESC"
            params = (search_id, f"%{search}%", f"%{search}%", f"%{search}%")
        else:
            query = "SELECT lawyer_id, name, specialization, email FROM lawyers ORDER BY lawyer_id DESC"
            params = ()

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params = params + (limit, offset)

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def count_lawyers(search=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            cursor.execute(
                "SELECT COUNT(*) FROM lawyers WHERE lawyer_id = %s OR name LIKE %s OR specialization LIKE %s OR email LIKE %s",
                (search_id, f"%{search}%", f"%{search}%", f"%{search}%"),
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM lawyers")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def update_lawyer(lawyer_id, name, specialization, email=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE lawyers SET name=%s, specialization=%s, email=%s WHERE lawyer_id=%s", (name, specialization, email, lawyer_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_lawyer(lawyer_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM cases WHERE lawyer_id=%s", (lawyer_id,))
        linked = cursor.fetchone()[0]
        if linked > 0:
            raise RuntimeError(f"Cannot delete lawyer with {linked} active case(s). Reassign or close cases first.")

        cursor.execute("DELETE FROM lawyers WHERE lawyer_id=%s", (lawyer_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


# SECURITY: Do not call get_cases() from lawyer/client routes

def get_cases(limit=None, offset=0, search=""):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            query = (
                "SELECT c.case_id, c.case_number, c.case_type, c.status, c.client_id, c.lawyer_id, c.filing_date, c.description "
                "FROM cases c "
                "LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id "
                "WHERE c.case_id = %s OR c.case_number LIKE %s OR c.case_type LIKE %s "
                "OR (COALESCE(cl.first_name, '') || ' ' || COALESCE(cl.last_name, '')) LIKE %s "
                "OR COALESCE(l.name, '') LIKE %s "
                "ORDER BY c.case_id DESC"
            )
            params = (search_id, f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%")
        else:
            query = "SELECT case_id, case_number, case_type, status, client_id, lawyer_id, filing_date, description FROM cases ORDER BY case_id DESC"
            params = ()

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params = params + (limit, offset)

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_cases_for_lawyer(lawyer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT case_id, case_number, case_type, status, filing_date FROM cases WHERE lawyer_id=%s ORDER BY case_id DESC",
            (lawyer_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_cases_for_client(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT case_id, case_number, case_type, status, filing_date FROM cases WHERE client_id=%s ORDER BY case_id DESC",
            (client_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def count_cases(search=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if search:
            search_id = int(search) if str(search).isdigit() else -1
            cursor.execute(
                "SELECT COUNT(*) FROM cases c "
                "LEFT JOIN clients cl ON c.client_id = cl.client_id "
                "LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id "
                "WHERE c.case_id = %s OR c.case_number LIKE %s OR c.case_type LIKE %s "
                "OR (COALESCE(cl.first_name, '') || ' ' || COALESCE(cl.last_name, '')) LIKE %s "
                "OR COALESCE(l.name, '') LIKE %s",
                (search_id, f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"),
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM cases")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def add_case(case_number, case_type, client_id, lawyer_id, filing_date, description):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO cases (case_number, case_type, client_id, lawyer_id, filing_date, description) VALUES (%s, %s, %s, %s, %s, %s)",
            (case_number, case_type, client_id, lawyer_id, filing_date, description),
        )
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_case_by_id_simple(case_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM cases WHERE case_id=%s", (case_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_case_by_id(case_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # SQLite only — use CONCAT() for MySQL
        cursor.execute(
            """
            SELECT
                c.case_id,
                c.case_number,
                c.case_type,
                c.status,
                c.filing_date,
                c.description,
                COALESCE(cl.first_name, '') || ' ' || COALESCE(cl.last_name, '') AS client_name,
                cl.email AS client_email,
                cl.phone AS client_phone,
                cl.address AS client_address,
                l.name AS lawyer_name,
                l.specialization AS lawyer_specialization
            FROM cases c
            LEFT JOIN clients cl ON c.client_id = cl.client_id
            LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id
            WHERE c.case_id = %s
            """,
            (case_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_all_cases():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # SQLite only — use CONCAT() for MySQL
        cursor.execute(
            """
            SELECT
                c.case_id,
                c.case_number,
                c.case_type,
                c.status,
                COALESCE(cl.first_name, '') || ' ' || COALESCE(cl.last_name, '') AS client_name,
                COALESCE(l.name, 'Unassigned') AS lawyer_name
            FROM cases c
            LEFT JOIN clients cl ON c.client_id = cl.client_id
            LEFT JOIN lawyers l ON c.lawyer_id = l.lawyer_id
            ORDER BY c.case_id DESC
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_case_history(case_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM case_history WHERE case_id=%s ORDER BY history_id DESC", (case_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def update_case(case_id, case_number=None, case_type=None, client_id=None, lawyer_id=None, filing_date=None, description=None, status=None, changed_by_role=None, changed_by_id=None):
    if status is not None and status not in ("Active", "Closed", "Pending"):
        raise ValueError("Invalid case status. Allowed: Active, Closed, Pending")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        existing = get_case_by_id_simple(case_id)
        if not existing:
            raise RuntimeError("Case not found")

        fields = []
        params = []
        changes = {}

        def add_change(field_name, value):
            if value is not None:
                old = existing.get(field_name)
                if str(old) != str(value):
                    fields.append(f"{field_name}=%s")
                    params.append(value)
                    changes[field_name] = {"old": old, "new": value}

        add_change("case_number", case_number)
        add_change("case_type", case_type)
        add_change("client_id", client_id)
        add_change("lawyer_id", lawyer_id)
        add_change("filing_date", filing_date)
        add_change("description", description)
        add_change("status", status)

        if not fields:
            return

        params.append(case_id)
        cursor.execute("UPDATE cases SET " + ", ".join(fields) + " WHERE case_id=%s", tuple(params))

        for key, value in changes.items():
            cursor.execute(
                "INSERT INTO case_history (case_id, changed_by_role, changed_by_id, field_name, old_value, new_value) VALUES (%s, %s, %s, %s, %s, %s)",
                (case_id, changed_by_role, changed_by_id, key, str(value["old"]), str(value["new"])),
            )

        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_case(case_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM cases WHERE case_id=%s", (case_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update_case_status(case_id, status):
    update_case(case_id, status=status)


def add_hearing(case_id, hearing_date, notes):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO hearings (case_id, hearing_date, notes) VALUES (%s, %s, %s)", (case_id, hearing_date, notes))
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_hearings(case_id=None, limit=None, offset=0):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if case_id is None:
            query = "SELECT hearing_id, case_id, hearing_date, notes FROM hearings ORDER BY hearing_id DESC"
            params = ()
        else:
            query = "SELECT hearing_id, case_id, hearing_date, notes FROM hearings WHERE case_id=%s ORDER BY hearing_id DESC"
            params = (case_id,)

        if limit is not None:
            query += " LIMIT %s OFFSET %s"
            params = params + (limit, offset)

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def count_hearings(case_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if case_id is None:
            cursor.execute("SELECT COUNT(*) FROM hearings")
        else:
            cursor.execute("SELECT COUNT(*) FROM hearings WHERE case_id=%s", (case_id,))
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def update_hearing(hearing_id, hearing_date=None, notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        fields = []
        params = []
        if hearing_date is not None:
            fields.append("hearing_date=%s")
            params.append(hearing_date)
        if notes is not None:
            fields.append("notes=%s")
            params.append(notes)
        if not fields:
            return
        params.append(hearing_id)
        cursor.execute("UPDATE hearings SET " + ", ".join(fields) + " WHERE hearing_id=%s", tuple(params))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete_hearing(hearing_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM hearings WHERE hearing_id=%s", (hearing_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM clients")
        clients = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM lawyers")
        lawyers = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM cases")
        cases = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM cases WHERE status='Active'")
        active_cases = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM hearings")
        hearings = cursor.fetchone()[0]
        return {
            "clients": clients,
            "lawyers": lawyers,
            "cases": cases,
            "active_cases": active_cases,
            "hearings": hearings,
        }
    finally:
        cursor.close()
        conn.close()


def add_feedback(case_id, author_role, author_id, rating, feedback_text):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO case_feedback (case_id, author_role, author_id, rating, feedback_text) VALUES (%s, %s, %s, %s, %s)",
            (case_id, author_role, author_id, rating, feedback_text),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_feedback_for_case(case_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT feedback_id, case_id, author_role, author_id, rating, feedback_text, created_at FROM case_feedback WHERE case_id=%s ORDER BY feedback_id DESC",
            (case_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def create_date_change_request(case_id, requested_by_role, requested_by_id, current_date, requested_date, reason):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO date_change_requests (case_id, requested_by_role, requested_by_id, current_date, requested_date, reason) VALUES (%s, %s, %s, %s, %s, %s)",
            (case_id, requested_by_role, requested_by_id, current_date, requested_date, reason),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_date_change_requests(status=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if status:
            cursor.execute("SELECT * FROM date_change_requests WHERE status=%s ORDER BY request_id DESC", (status,))
        else:
            cursor.execute("SELECT * FROM date_change_requests ORDER BY request_id DESC")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_date_change_request_by_id(request_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM date_change_requests WHERE request_id=%s", (request_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def resolve_date_change_request(request_id, status, court_note=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE date_change_requests SET status=%s, court_note=%s, resolved_at=datetime('now') WHERE request_id=%s",
            (status, court_note, request_id),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def apply_date_change_to_case_hearing(case_id, new_date):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Update all date references for this case after court approval.
        cursor.execute("UPDATE cases SET filing_date=%s WHERE case_id=%s", (new_date, case_id))
        cursor.execute("UPDATE hearings SET hearing_date=%s WHERE case_id=%s", (new_date, case_id))

        # If the case has no hearing row, create one so date state is visible everywhere.
        cursor.execute("SELECT COUNT(*) FROM hearings WHERE case_id=%s", (case_id,))
        hearing_count = cursor.fetchone()[0]
        if hearing_count == 0:
            cursor.execute(
                "INSERT INTO hearings (case_id, hearing_date, notes) VALUES (%s, %s, %s)",
                (case_id, new_date, "Date changed by court approval"),
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def create_notification(recipient_role, recipient_id, title, message, case_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO notifications (recipient_role, recipient_id, case_id, title, message) VALUES (%s, %s, %s, %s, %s)",
            (recipient_role, recipient_id, case_id, title, message),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def create_case_notifications(case_id, title, message, include_court=True):
    case_row = get_case_by_id_simple(case_id)
    if not case_row:
        return
    if include_court:
        create_notification("court", 1, title, message, case_id)
    if case_row.get("lawyer_id"):
        create_notification("lawyer", int(case_row.get("lawyer_id")), title, message, case_id)
    if case_row.get("client_id"):
        create_notification("client", int(case_row.get("client_id")), title, message, case_id)


def get_notifications(recipient_role, recipient_id, limit=100):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT notification_id, recipient_role, recipient_id, case_id, title, message, is_read, created_at "
            "FROM notifications WHERE recipient_role=%s AND recipient_id=%s ORDER BY notification_id DESC LIMIT %s",
            (recipient_role, recipient_id, limit),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def mark_notification_read(notification_id, recipient_role, recipient_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read=1 WHERE notification_id=%s AND recipient_role=%s AND recipient_id=%s",
            (notification_id, recipient_role, recipient_id),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def mark_all_notifications_read(recipient_role, recipient_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE notifications SET is_read=1 WHERE recipient_role=%s AND recipient_id=%s",
            (recipient_role, recipient_id),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


