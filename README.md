# Contact App

A small browser-based contact app built with Python, Flask, and SQLite. Save first and last names, email, phone, city, and state; search saved contacts and remove entries you no longer need. The database is created automatically in the `instance` folder.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. On Windows, if `py` is unavailable, replace it with `python` in the first command.