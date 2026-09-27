import os
import sqlite3

from flask import Flask, flash, g, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-key")
app.config["DATABASE"] = os.path.join(app.instance_path, "entries.sqlite")

def get_db():
    if "db" not in g:
        os.makedirs(app.instance_path, exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    database = get_db()
    columns = {
        row["name"] for row in database.execute("PRAGMA table_info(entries)").fetchall()
    }

    if not columns:
        create_entries_table(database)
    elif "first_name" not in columns:
        database.execute("ALTER TABLE entries RENAME TO entries_legacy")
        create_entries_table(database)
        old_entries = database.execute(
            "SELECT * FROM entries_legacy ORDER BY id"
        ).fetchall()
        for entry in old_entries:
            name_parts = entry["name"].strip().split(maxsplit=1)
            first_name = name_parts[0] if name_parts else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            database.execute(
                """
                INSERT INTO entries
                    (id, first_name, last_name, email, phone, city, state, created_at)
                VALUES (?, ?, ?, ?, '', '', '', ?)
                """,
                (entry["id"], first_name, last_name, entry["email"], entry["created_at"]),
            )
    database.commit()


def create_entries_table(database):
    database.execute(
        """
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL DEFAULT '',
            city TEXT NOT NULL DEFAULT '',
            state TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


@app.teardown_appcontext
def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()

        if not first_name or not last_name or not email:
            flash("Add a first name, last name, and email before saving.", "error")
            return render_template(
                "index.html",
                entries=get_entries(),
                total_count=get_count(),
                form_data=request.form,
            ), 400

        database = get_db()
        database.execute(
            """
            INSERT INTO entries (first_name, last_name, email, phone, city, state)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (first_name, last_name, email, phone, city, state),
        )
        database.commit()
        flash("Entry saved.", "success")
        return redirect(url_for("index"))

    return render_page()


def get_entries():
    search = request.args.get("q", "").strip()
    conditions = []
    parameters = []

    if search:
        match = f"%{search}%"
        conditions.append(
            "(first_name LIKE ? OR last_name LIKE ? OR email LIKE ? "
            "OR phone LIKE ? OR city LIKE ? OR state LIKE ?)"
        )
        parameters.extend((match, match, match, match, match, match))

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    return get_db().execute(
        f"SELECT * FROM entries {where_clause} "
        "ORDER BY last_name COLLATE NOCASE, first_name COLLATE NOCASE, id DESC",
        parameters,
    ).fetchall()


def get_count():
    return get_db().execute("SELECT COUNT(*) FROM entries").fetchone()[0]


def render_page():
    return render_template(
        "index.html",
        entries=get_entries(),
        total_count=get_count(),
        form_data={},
    )


@app.post("/entries/<int:entry_id>/delete")
def delete_entry(entry_id):
    database = get_db()
    database.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    database.commit()
    flash("Entry deleted.", "success")
    return redirect(url_for("index"))


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)