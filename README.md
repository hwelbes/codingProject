# Contact App

Contact App is a small browser-based contact directory built with Python, Flask, and SQLite. Add a contact, search the directory, and delete contacts you no longer need. The app is designed to run locally on your computer.

## Features

- Save a contact's first name, last name, email, phone, city, and state.
- Require first name, last name, and a valid email address; phone, city, and state are optional.
- Search contacts by first name, last name, email, phone, city, or state.
- View contacts in last-name, then first-name order.
- Delete a contact after confirming the action.
- Keep records between runs in a local SQLite database.

## Requirements

- Python 3.10 or newer
- pip

Flask is installed from `requirements.txt`.

## Install and run on Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Keep the terminal running while using the app; press `Ctrl+C` there to stop the server. If the `py` launcher is unavailable, use `python` instead.

## Use the App

1. Enter the contact's first name, last name, and email address.
2. Optionally add a phone number, city, and state.
3. Select **Save entry**. The contact appears in the directory.
4. Search by any saved contact field using the search box.
5. Select **Delete** next to a contact and confirm to remove it.

## Data and Migration

The app creates its database at `instance/entries.sqlite` the first time it starts. The `instance/` directory is local runtime data and is excluded from version control. Back up this SQLite file if you need to preserve contacts when moving or reinstalling the project.

When an older database with full-name, category, date, and notes fields is detected, the app creates the new contact table and copies the old records. It splits each full name at the first space into first and last name, and carries over the email. Other old fields remain in the renamed `entries_legacy` table; they are not shown in the contact directory.

## Project layout

```text
app.py                      Flask routes, validation, SQLite access, and migration
templates/index.html        Contact form and directory page
static/styles.css           Responsive page styling
requirements.txt            Python package dependencies
instance/entries.sqlite     Local contact database, created at runtime
```

## Development note

`python app.py` starts Flask with debug mode enabled for local development. Do not expose this development server to the public internet or use it as a production deployment server.