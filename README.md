# TecW Rocódromo

Flask web application for managing a climbing gym — ways (vías), bouldering blocks (bloques) and members (usuarios).

---

## Project structure

```
tecw_yo/
├── tecw_02_flask/
│   └── app/
│       ├── app.py              # Application factory & entry point
│       ├── db.py               # SQLAlchemy instance
│       ├── data.py             # Fixture data for seeders
│       ├── access_control.py   # Auth & role decorators
│       ├── handle_files.py     # File upload decorator
│       ├── blueprints/         # Routes: common, auth, ways, blocks, users
│       ├── models/             # ORM models + migrations + seeders
│       ├── templates/          # Jinja2 HTML templates
│       └── public/             # Static assets (CSS, JS, images)
└── requirements.txt
```

---

## Requirements

- Python 3.10+
- pip

---

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set the Flask app environment variable**

```bash
export FLASK_APP=tecw_02_flask/app/app.py      # macOS / Linux
set FLASK_APP=tecw_02_flask/app/app.py         # Windows
```

---

## Running the app

```bash
flask run
```

The app will be available at `http://127.0.0.1:5000`.

For debug mode:

```bash
flask run --debug
```

---

## Database

### Apply migrations

Run all pending Alembic migrations to bring the database schema up to date:

```bash
flask db upgrade
```

### Seed the database

Populate the database with the initial fixture data (users, ways and blocks):

```bash
flask seed
```

> Default credentials for the seeded admin account:
> **Email:** `admin@tecw.es` — **Password:** `password`

### Reset the database

Drop all tables and recreate them from scratch (**destructive — dev only**):

```bash
flask reset-db
```

After a reset, run migrations and seed again:

```bash
flask db upgrade
flask seed
```

---

## Alembic / Flask-Migrate reference

| Command | Description |
|---|---|
| `flask db init` | Initialise the migrations folder (run once) |
| `flask db migrate -m "message"` | Auto-generate a new migration from model changes |
| `flask db upgrade` | Apply all pending migrations |
| `flask db downgrade` | Revert the last migration |
| `flask db downgrade base` | Revert all migrations back to the initial state |
| `flask db history` | Show the full migration history |
| `flask db current` | Show the currently applied migration revision |

---

## Roles

| Role | Permissions |
|---|---|
| `admin` | Full CRUD on ways, blocks and users |
| `user` | Read-only on ways and blocks; can edit and delete their own profile |
