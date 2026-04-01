import csv
import io
import os
import re
import secrets
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    Response,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from db import ensure_tables_exist, test_connection
from operations import (
    add_case,
    add_client,
    add_hearing,
    add_lawyer,
    count_cases,
    count_clients,
    count_hearings,
    count_lawyers,
    delete_case,
    delete_client,
    delete_hearing,
    delete_lawyer,
    get_audit_logs,
    get_all_cases,
    get_case_by_id,
    get_case_by_id_simple,
    get_case_history,
    get_cases,
    get_clients,
    get_dashboard_stats,
    get_hearings,
    get_lawyers,
    get_notifications,
    get_user_id_by_email,
    get_feedback_for_case,
    add_feedback,
    create_case_notifications,
    create_date_change_request,
    get_date_change_requests,
    get_date_change_request_by_id,
    resolve_date_change_request,
    apply_date_change_to_case_hearing,
    mark_notification_read,
    mark_all_notifications_read,
    log_action,
    update_case,
    update_client,
    update_hearing,
    update_lawyer,
)
from service import client_dashboard, court_dashboard, lawyer_dashboard, login as service_login, register as service_register


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "legal-case-dev-secret")
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", "0") == "1"

_db_checked = False


def validate_required(fields_dict):
    for field, value in fields_dict.items():
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field} is required")


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email or ""):
        raise ValueError("Invalid email format")


def validate_date_ymd(date_value):
    datetime.strptime(date_value, "%Y-%m-%d")


def is_logged_in():
    return "role" in session and "user_id" in session


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_logged_in():
                return redirect(url_for("login"))
            if session.get("role") not in roles:
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def verify_csrf():
    form_token = request.form.get("csrf_token")
    if not form_token or form_token != session.get("csrf_token"):
        abort(403)


def current_notification_target():
    if not is_logged_in():
        return None, None
    return session.get("role"), int(session.get("user_id") or 0)


@app.before_request
def app_init_and_csrf_setup():
    global _db_checked
    if not _db_checked:
        ensure_tables_exist()
        ok, _ = test_connection()
        if not ok:
            abort(500)
        _db_checked = True

    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)


@app.context_processor
def inject_helpers():
    def csrf_input():
        return f'<input type="hidden" name="csrf_token" value="{session.get("csrf_token", "")}">' 

    return {"csrf_input": csrf_input}


@app.route("/")
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    role = session.get("role")
    if role == "court":
        return redirect(url_for("court_dashboard_page"))
    if role == "lawyer":
        return redirect(url_for("lawyer_dashboard_page"))
    return redirect(url_for("client_dashboard_page"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        verify_csrf()
        role = request.form.get("role", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        try:
            validate_required({"role": role, "username": username, "password": password})
        except ValueError as e:
            flash(str(e), "error")
            return render_template("login.html")

        if not service_login(role, username, password):
            flash("Invalid credentials", "error")
            return render_template("login.html")

        session["role"] = role
        session["username"] = username
        if role == "court":
            session["user_id"] = 1
        else:
            session["user_id"] = get_user_id_by_email(role, username) or 0

        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/register/client", methods=["GET", "POST"])
def register_client_page():
    if request.method == "POST":
        verify_csrf()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()
        try:
            validate_required(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "address": address,
                    "password": password,
                    "confirm_password": confirm,
                }
            )
            validate_email(email)
            if password != confirm:
                raise ValueError("Passwords do not match")
            service_register(
                "client",
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                password=password,
            )
            flash("Client registered successfully. Please login.", "ok")
            return redirect(url_for("login"))
        except Exception as e:
            flash(str(e), "error")
    return render_template("register_client.html")


@app.route("/register/lawyer", methods=["GET", "POST"])
def register_lawyer_page():
    if request.method == "POST":
        verify_csrf()
        name = request.form.get("name", "").strip()
        specialization = request.form.get("specialization", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()
        try:
            validate_required(
                {
                    "name": name,
                    "specialization": specialization,
                    "email": email,
                    "password": password,
                    "confirm_password": confirm,
                }
            )
            validate_email(email)
            if password != confirm:
                raise ValueError("Passwords do not match")
            service_register("lawyer", name=name, specialization=specialization, email=email, password=password)
            flash("Lawyer registered successfully. Please login.", "ok")
            return redirect(url_for("login"))
        except Exception as e:
            flash(str(e), "error")
    return render_template("register_lawyer.html")


@app.route("/dashboard/court")
@role_required("court")
def court_dashboard_page():
    return render_template("dashboard_court.html", stats=court_dashboard())


@app.route("/dashboard/lawyer")
@role_required("lawyer")
def lawyer_dashboard_page():
    return render_template("dashboard_lawyer.html", data=lawyer_dashboard(session.get("user_id")))


@app.route("/dashboard/client")
@role_required("client")
def client_dashboard_page():
    return render_template("dashboard_client.html", data=client_dashboard(session.get("user_id")))


@app.route("/clients", methods=["GET", "POST"])
@role_required("court")
def clients_page():
    if request.method == "POST":
        verify_csrf()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        try:
            validate_required({"first_name": first_name, "last_name": last_name, "email": email})
            validate_email(email)
            add_client(first_name, last_name, email, phone, address)
            log_action(session.get("role"), session.get("user_id"), "CREATE", "client", None, {"email": email})
            flash("Client added (no login credentials). The client must register themselves.", "ok")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("clients_page"))

    page = max(1, int(request.args.get("page", 1)))
    per_page = 20
    q = request.args.get("q", "").strip()
    total = count_clients(q)
    total_pages = max(1, (total + per_page - 1) // per_page)
    clients = get_clients(limit=per_page, offset=(page - 1) * per_page, search=q)
    return render_template("clients.html", clients=clients, page=page, total_pages=total_pages, q=q)


@app.route("/clients/<int:client_id>/edit", methods=["POST"])
@role_required("court")
def edit_client_page(client_id):
    verify_csrf()
    try:
        update_client(
            client_id,
            request.form.get("first_name", "").strip(),
            request.form.get("last_name", "").strip(),
            request.form.get("email", "").strip(),
            request.form.get("phone", "").strip(),
            request.form.get("address", "").strip(),
        )
        log_action(session.get("role"), session.get("user_id"), "UPDATE", "client", client_id, {"message": "client updated"})
        flash("Client updated", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("clients_page"))


@app.route("/clients/<int:client_id>/delete", methods=["POST"])
@role_required("court")
def delete_client_page(client_id):
    verify_csrf()
    try:
        delete_client(client_id)
        log_action(session.get("role"), session.get("user_id"), "DELETE", "client", client_id, {})
        flash("Client deleted", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("clients_page"))


@app.route("/lawyers", methods=["GET", "POST"])
@role_required("court")
def lawyers_page():
    if request.method == "POST":
        verify_csrf()
        try:
            add_lawyer(request.form.get("name", "").strip(), request.form.get("specialization", "").strip())
            log_action(session.get("role"), session.get("user_id"), "CREATE", "lawyer", None, {"name": request.form.get("name", "")})
            flash("Lawyer added", "ok")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("lawyers_page"))

    page = max(1, int(request.args.get("page", 1)))
    per_page = 20
    q = request.args.get("q", "").strip()
    total = count_lawyers(q)
    total_pages = max(1, (total + per_page - 1) // per_page)
    lawyers = get_lawyers(limit=per_page, offset=(page - 1) * per_page, search=q)
    return render_template("lawyers.html", lawyers=lawyers, page=page, total_pages=total_pages, q=q)


@app.route("/lawyers/<int:lawyer_id>/edit", methods=["POST"])
@role_required("court")
def edit_lawyer_page(lawyer_id):
    verify_csrf()
    try:
        update_lawyer(
            lawyer_id,
            request.form.get("name", "").strip(),
            request.form.get("specialization", "").strip(),
            request.form.get("email", "").strip(),
        )
        log_action(session.get("role"), session.get("user_id"), "UPDATE", "lawyer", lawyer_id, {"message": "lawyer updated"})
        flash("Lawyer updated", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("lawyers_page"))


@app.route("/lawyers/<int:lawyer_id>/delete", methods=["POST"])
@role_required("court")
def delete_lawyer_page(lawyer_id):
    verify_csrf()
    try:
        delete_lawyer(lawyer_id)
        log_action(session.get("role"), session.get("user_id"), "DELETE", "lawyer", lawyer_id, {})
        flash("Lawyer deleted", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("lawyers_page"))


@app.route("/cases", methods=["GET", "POST"])
@role_required("court")
def cases_page():
    if request.method == "POST":
        verify_csrf()
        case_number = request.form.get("case_number", "").strip()
        case_type = request.form.get("case_type", "").strip()
        client_id = int(request.form.get("client_id", "0") or 0)
        lawyer_id = int(request.form.get("lawyer_id", "0") or 0)
        filing_date = request.form.get("filing_date", "").strip()
        description = request.form.get("description", "").strip()

        try:
            validate_required({"case_number": case_number, "case_type": case_type, "filing_date": filing_date})
            validate_date_ymd(filing_date)
            add_case(case_number, case_type, client_id, lawyer_id, filing_date, description)
            log_action(session.get("role"), session.get("user_id"), "CREATE", "case", None, {"case_number": case_number})
            # Notify all parties about newly added case
            latest_case = get_cases(limit=1, offset=0)
            if latest_case:
                case_id = latest_case[0].get("case_id")
                create_case_notifications(case_id, "Case Added", f"Case {case_number} has been added.")
            flash("Case created", "ok")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("cases_page"))

    page = max(1, int(request.args.get("page", 1)))
    per_page = 20
    q = request.args.get("q", "").strip()
    total = count_cases(q)
    total_pages = max(1, (total + per_page - 1) // per_page)

    return render_template(
        "cases.html",
        cases=get_cases(limit=per_page, offset=(page - 1) * per_page, search=q),
        clients=get_clients(),
        lawyers=get_lawyers(),
        page=page,
        total_pages=total_pages,
        q=q,
    )


@app.route("/cases/<int:case_id>/edit", methods=["POST"])
@role_required("court")
def edit_case_page(case_id):
    verify_csrf()
    try:
        update_case(
            case_id,
            case_number=request.form.get("case_number", "").strip(),
            case_type=request.form.get("case_type", "").strip(),
            client_id=int(request.form.get("client_id", "0") or 0),
            lawyer_id=int(request.form.get("lawyer_id", "0") or 0),
            filing_date=request.form.get("filing_date", "").strip(),
            description=request.form.get("description", "").strip(),
            status=request.form.get("status", "").strip(),
            changed_by_role=session.get("role"),
            changed_by_id=session.get("user_id"),
        )
        log_action(session.get("role"), session.get("user_id"), "UPDATE", "case", case_id, {"message": "case updated"})
        create_case_notifications(case_id, "Case Updated", f"Case #{case_id} was updated.")
        flash("Case updated", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("cases_page"))


@app.route("/cases/<int:case_id>/delete", methods=["POST"])
@role_required("court")
def delete_case_page(case_id):
    verify_csrf()
    try:
        delete_case(case_id)
        log_action(session.get("role"), session.get("user_id"), "DELETE", "case", case_id, {})
        flash("Case deleted", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("cases_page"))


@app.route("/cases/<int:case_id>/history")
@role_required("court")
def case_history_page(case_id):
    case_item = get_case_by_id(case_id)
    history = get_case_history(case_id)
    return render_template("case_history.html", case_item=case_item, history=history)


@app.route("/cases/<int:case_id>/view")
@role_required("court", "lawyer", "client")
def view_case_page(case_id):
    case_item = get_case_by_id(case_id)
    case_raw = get_case_by_id_simple(case_id)
    if not case_item or not case_raw:
        abort(404)

    role = session.get("role")
    user_id = int(session.get("user_id") or 0)

    if role == "lawyer" and int(case_raw.get("lawyer_id") or 0) != user_id:
        abort(403)
    if role == "client" and int(case_raw.get("client_id") or 0) != user_id:
        abort(403)

    hearings = get_hearings(case_id=case_id)
    feedback_items = get_feedback_for_case(case_id)
    return render_template("case_detail.html", case_item=case_item, hearings=hearings, feedback_items=feedback_items)


@app.route("/cases/<int:case_id>/feedback", methods=["POST"])
@role_required("lawyer", "client")
def add_case_feedback_page(case_id):
    verify_csrf()
    case_raw = get_case_by_id_simple(case_id)
    if not case_raw:
        abort(404)

    role = session.get("role")
    user_id = int(session.get("user_id") or 0)
    if role == "lawyer" and int(case_raw.get("lawyer_id") or 0) != user_id:
        abort(403)
    if role == "client" and int(case_raw.get("client_id") or 0) != user_id:
        abort(403)

    rating = int(request.form.get("rating", "0") or 0)
    feedback_text = request.form.get("feedback_text", "").strip()
    try:
        validate_required({"feedback_text": feedback_text})
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        add_feedback(case_id, role, user_id, rating, feedback_text)
        log_action(role, user_id, "CREATE", "feedback", case_id, {"rating": rating})
        create_case_notifications(case_id, "New Feedback", f"New feedback added by {role} on case #{case_id}.")
        flash("Feedback submitted", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("view_case_page", case_id=case_id))


@app.route("/cases/<int:case_id>/request-date-change", methods=["POST"])
@role_required("lawyer", "client")
def request_date_change_page(case_id):
    verify_csrf()
    case_raw = get_case_by_id_simple(case_id)
    if not case_raw:
        abort(404)

    role = session.get("role")
    user_id = int(session.get("user_id") or 0)
    if role == "lawyer" and int(case_raw.get("lawyer_id") or 0) != user_id:
        abort(403)
    if role == "client" and int(case_raw.get("client_id") or 0) != user_id:
        abort(403)

    requested_date = request.form.get("requested_date", "").strip()
    reason = request.form.get("reason", "").strip()
    try:
        validate_required({"requested_date": requested_date, "reason": reason})
        validate_date_ymd(requested_date)
        create_date_change_request(
            case_id=case_id,
            requested_by_role=role,
            requested_by_id=user_id,
            current_date=(case_raw.get("filing_date") or ""),
            requested_date=requested_date,
            reason=reason,
        )
        log_action(role, user_id, "CREATE", "date_change_request", case_id, {"requested_date": requested_date})
        create_case_notifications(case_id, "Date Change Requested", f"{role.title()} requested date change for case #{case_id}.")
        flash("Date change request submitted to court", "ok")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("view_case_page", case_id=case_id))


@app.route("/hearings", methods=["GET", "POST"])
@role_required("court")
def hearings_page():
    if request.method == "POST":
        verify_csrf()
        try:
            add_hearing(
                int(request.form.get("case_id", "0") or 0),
                request.form.get("hearing_date", "").strip(),
                request.form.get("notes", "").strip(),
            )
            case_id = int(request.form.get("case_id", "0") or 0)
            log_action(session.get("role"), session.get("user_id"), "CREATE", "hearing", None, {"case_id": request.form.get("case_id")})
            create_case_notifications(case_id, "Hearing Added", f"Hearing added for case #{case_id}.")
            flash("Hearing added", "ok")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("hearings_page"))

    page = max(1, int(request.args.get("page", 1)))
    per_page = 20
    total = count_hearings()
    total_pages = max(1, (total + per_page - 1) // per_page)
    hearings = get_hearings(limit=per_page, offset=(page - 1) * per_page)
    return render_template("hearings.html", hearings=hearings, cases=get_cases(), page=page, total_pages=total_pages)


@app.route("/hearings/<int:hearing_id>/edit", methods=["POST"])
@role_required("court")
def edit_hearing_page(hearing_id):
    verify_csrf()
    try:
        update_hearing(hearing_id, hearing_date=request.form.get("hearing_date", "").strip(), notes=request.form.get("notes", "").strip())
        # Identify case for notification
        all_hearings = get_hearings()
        case_id = next((h.get("case_id") for h in all_hearings if h.get("hearing_id") == hearing_id), None)
        log_action(session.get("role"), session.get("user_id"), "UPDATE", "hearing", hearing_id, {"message": "hearing updated"})
        if case_id:
            create_case_notifications(case_id, "Hearing Updated", f"Hearing #{hearing_id} notes/date changed.")
        flash("Hearing updated", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("hearings_page"))


@app.route("/hearings/<int:hearing_id>/delete", methods=["POST"])
@role_required("court")
def delete_hearing_page(hearing_id):
    verify_csrf()
    try:
        delete_hearing(hearing_id)
        log_action(session.get("role"), session.get("user_id"), "DELETE", "hearing", hearing_id, {})
        flash("Hearing deleted", "ok")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("hearings_page"))


@app.route("/audit")
@role_required("court")
def audit_page():
    return render_template("audit.html", logs=get_audit_logs())


@app.route("/date-change-requests")
@role_required("court")
def date_change_requests_page():
    status = request.args.get("status", "")
    requests = get_date_change_requests(status if status else None)
    return render_template("date_change_requests.html", requests=requests, status=status)


@app.route("/date-change-requests/<int:request_id>/resolve", methods=["POST"])
@role_required("court")
def resolve_date_change_request_page(request_id):
    verify_csrf()
    status = request.form.get("status", "").strip()
    court_note = request.form.get("court_note", "").strip()
    req = get_date_change_request_by_id(request_id)
    if not req:
        abort(404)
    if status not in ("Approved", "Rejected"):
        flash("Invalid status", "error")
        return redirect(url_for("date_change_requests_page"))

    resolve_date_change_request(request_id, status, court_note)
    if status == "Approved":
        apply_date_change_to_case_hearing(req.get("case_id"), req.get("requested_date"))
    create_case_notifications(
        req.get("case_id"),
        f"Date Change {status}",
        f"Date change request for case #{req.get('case_id')} was {status.lower()}."
    )
    log_action(session.get("role"), session.get("user_id"), "UPDATE", "date_change_request", request_id, {"status": status})
    flash(f"Request {status.lower()}.", "ok")
    return redirect(url_for("date_change_requests_page"))


@app.route("/notifications")
@role_required("court", "lawyer", "client")
def notifications_page():
    role, user_id = current_notification_target()
    notifications = get_notifications(role, user_id)
    return render_template("notifications.html", notifications=notifications)


@app.route("/notifications/read-all", methods=["POST"])
@role_required("court", "lawyer", "client")
def notifications_read_all_page():
    verify_csrf()
    role, user_id = current_notification_target()
    mark_all_notifications_read(role, user_id)
    flash("All notifications marked as read", "ok")
    return redirect(url_for("notifications_page"))


@app.route("/notifications/<int:notification_id>/read", methods=["POST"])
@role_required("court", "lawyer", "client")
def notifications_read_one_page(notification_id):
    verify_csrf()
    role, user_id = current_notification_target()
    mark_notification_read(notification_id, role, user_id)
    return redirect(url_for("notifications_page"))


@app.route("/export/cases")
@role_required("court")
def export_cases():
    data = get_cases()
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["case_id", "case_number", "case_type", "status", "filing_date"])
    writer.writeheader()
    for row in data:
        writer.writerow(
            {
                "case_id": row.get("case_id"),
                "case_number": row.get("case_number"),
                "case_type": row.get("case_type"),
                "status": row.get("status"),
                "filing_date": row.get("filing_date"),
            }
        )
    return Response(buf.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=cases.csv"})


@app.route("/api/cases")
def api_cases():
    auth = request.authorization
    if not auth or not service_login("court", auth.username, auth.password):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_cases())


@app.route("/api/cases/<int:case_id>")
def api_case_by_id(case_id):
    auth = request.authorization
    if not auth or not service_login("court", auth.username, auth.password):
        return jsonify({"error": "Unauthorized"}), 401
    case_item = get_case_by_id(case_id)
    if not case_item:
        return jsonify({"error": "Case not found"}), 404
    return jsonify(case_item)


@app.route("/api/hearings")
def api_hearings():
    auth = request.authorization
    if not auth or not service_login("court", auth.username, auth.password):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(get_hearings())


@app.errorhandler(403)
def forbidden(_e):
    return render_template("error.html", code=403, message="Access Denied"), 403


@app.errorhandler(404)
def not_found(_e):
    return render_template("error.html", code=404, message="Page Not Found"), 404


@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"500 error: {e}")
    return render_template("error.html", code=500, message="Internal Server Error"), 500


if __name__ == "__main__":
    ensure_tables_exist()
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    app.run(host=host, port=port, debug=app.config["DEBUG"])
