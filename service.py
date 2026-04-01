import hashlib
import os

from operations import (
    authenticate_user,
    register_client,
    register_lawyer,
    get_dashboard_stats,
    get_connection,
    get_cases_for_lawyer,
    get_cases_for_client,
)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _court_credentials():
    username = os.environ.get("COURT_USERNAME", "court_admin")
    password = os.environ.get("COURT_PASSWORD", "court_secret")
    return username, _hash_password(password)


def login(role, email_or_username, password):
    if role == "court":
        username, password_hash = _court_credentials()
        return email_or_username == username and _hash_password(password) == password_hash
    if role in ("client", "lawyer"):
        return authenticate_user(role, email_or_username, password)
    return False


def register(role, **kwargs):
    if role == "client":
        return register_client(
            kwargs.get("first_name"),
            kwargs.get("last_name"),
            kwargs.get("email"),
            kwargs.get("phone"),
            kwargs.get("address"),
            kwargs.get("password"),
        )
    if role == "lawyer":
        return register_lawyer(
            kwargs.get("name"),
            kwargs.get("specialization"),
            kwargs.get("email"),
            kwargs.get("password"),
        )
    raise RuntimeError("Unsupported role for registration")


def court_dashboard():
    return get_dashboard_stats()


def lawyer_dashboard(lawyer_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM cases WHERE lawyer_id=%s", (lawyer_id,))
        cases_assigned = cursor.fetchone().get("total", 0)
        cursor.execute(
            "SELECT h.hearing_id, h.case_id, h.hearing_date, h.notes FROM hearings h "
            "JOIN cases c ON h.case_id = c.case_id WHERE c.lawyer_id=%s ORDER BY h.hearing_date DESC",
            (lawyer_id,),
        )
        hearings = cursor.fetchall()
        assigned_cases = get_cases_for_lawyer(lawyer_id)
        return {"cases_assigned": cases_assigned, "hearings": hearings, "assigned_cases": assigned_cases}
    finally:
        cursor.close()
        conn.close()


def client_dashboard(client_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM cases WHERE client_id=%s", (client_id,))
        total_cases = cursor.fetchone().get("total", 0)
        cursor.execute(
            "SELECT h.hearing_id, h.case_id, h.hearing_date, h.notes FROM hearings h "
            "JOIN cases c ON h.case_id = c.case_id WHERE c.client_id=%s ORDER BY h.hearing_date DESC",
            (client_id,),
        )
        hearings = cursor.fetchall()
        my_cases = get_cases_for_client(client_id)
        return {"cases": total_cases, "hearings": hearings, "my_cases": my_cases}
    finally:
        cursor.close()
        conn.close()
