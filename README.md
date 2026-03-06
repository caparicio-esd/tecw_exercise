# TecW Rocódromo

Flask REST API for managing a climbing gym — ways (vías), bouldering blocks (bloques), places (sectores), assets (media) and members (usuarios).

---

## Project structure

```
tecw_yo/
├── tecw_02_flask/               # Phase 2 — server-rendered Flask app (Jinja2)
└── tecw_03_restful_api/         # Phase 3 — JSON REST API (current)
    └── app/
        ├── app.py               # Application factory & entry point
        ├── db.py                # SQLAlchemy instance
        ├── auth/                # JWT helpers & decorators
        ├── blueprints/          # Routes per resource
        ├── dtos/                # Pydantic DTOs (validation + serialisation)
        ├── models/              # SQLAlchemy ORM models
        ├── migrations/          # Alembic migrations
        ├── seeders/             # Fixture data loaders
        └── fixtures/            # Raw fixture data
```

---

## Requirements

- Python 3.10+
- pip

---

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the API

```bash
flask --app tecw_03_restful_api/app/app.py run --debug
```

The API will be available at `http://127.0.0.1:5000`.

---

## Interactive documentation

| URL | UI |
|---|---|
| `http://localhost:5000/docs` | Swagger UI |
| `http://localhost:5000/docs/redoc` | Redoc |
| `http://localhost:5000/docs/rapidoc` | RapiDoc |
| `http://localhost:5000/docs/scalar` | Scalar |
| `http://localhost:5000/docs/openapi.json` | OpenAPI 3.1 spec (JSON) |

---

## Database

**Apply migrations**

```bash
flask --app tecw_03_restful_api/app/app.py db upgrade
```

**Seed the database**

```bash
flask --app tecw_03_restful_api/app/app.py seed
```

> Default admin credentials: **Email:** `admin@tecw.es` — **Password:** `password`

**Reset the database** (destructive — dev only)

```bash
flask --app tecw_03_restful_api/app/app.py reset-db
flask --app tecw_03_restful_api/app/app.py db upgrade
flask --app tecw_03_restful_api/app/app.py seed
```

---

## Authentication

The API uses **OAuth 2.0 password grant** with short-lived JWT access tokens and rotating refresh tokens.

### 1 — Obtain a token

```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "grant_type": "password",
  "username": "admin@tecw.es",
  "password": "password"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "expires_in": 900,
  "refresh_token": "<opaque-token>"
}
```

### 2 — Use the token

Add the `Authorization` header to every protected request:

```http
Authorization: Bearer <access_token>
```

### 3 — Refresh the token

When the access token expires, use the refresh token to get a new pair:

```http
POST /api/v1/auth/token
Content-Type: application/json

{
  "grant_type": "refresh_token",
  "refresh_token": "<refresh_token>"
}
```

### 4 — Revoke the refresh token

```http
POST /api/v1/auth/revoke
Content-Type: application/json

{
  "token": "<refresh_token>"
}
```

### In Swagger UI

Click **Authorize** (top right), enter `<access_token>` (without `Bearer `), and all protected endpoints will send the header automatically.

---

## API routes

Base URL: `/api/v1`

### Auth

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/token` | — | Get access + refresh token |
| POST | `/auth/revoke` | — | Revoke a refresh token |

### Ways `/ways`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/ways` | — | List ways (paginated, filterable, sortable) |
| GET | `/ways/{id}` | — | Get a single way |
| POST | `/ways` | Bearer | Create a way |
| PUT | `/ways/{id}` | Bearer | Update a way |
| DELETE | `/ways/{id}` | Bearer | Delete a way |

**Query filters:** `name` (like), `grade`, `type`, `city`, `active`
**Sort by:** `id`, `name`, `grade`, `length`, `city`

### Blocks `/blocks`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/blocks` | — | List blocks (paginated, filterable, sortable) |
| GET | `/blocks/{id}` | — | Get a single block |
| POST | `/blocks` | Bearer | Create a block |
| PUT | `/blocks/{id}` | Bearer | Update a block |
| DELETE | `/blocks/{id}` | Bearer | Delete a block |

**Query filters:** `name` (like), `grade`, `color`, `sector`, `city`, `active`
**Sort by:** `id`, `name`, `grade`, `height`, `city`

### Places `/places`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/places` | — | List places (paginated, filterable, sortable) |
| GET | `/places/{id}` | — | Get a single place |
| POST | `/places` | Bearer | Create a place |
| PUT | `/places/{id}` | Bearer | Update a place |
| DELETE | `/places/{id}` | Bearer | Delete a place |

**Query filters:** `name` (like)
**Sort by:** `id`, `name`

### Assets `/assets`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/assets` | — | List assets (paginated, filterable, sortable) |
| GET | `/assets/{id}` | — | Get a single asset |
| POST | `/assets` | Bearer | Register an asset |
| DELETE | `/assets/{id}` | Bearer | Delete an asset |

**Query filters:** `url` (like)
**Sort by:** `id`, `url`

### Users `/users`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/users` | — | List users (paginated, filterable, sortable) |
| GET | `/users/{id}` | — | Get a single user |
| POST | `/users` | Bearer | Create a user |
| PUT | `/users/{id}` | Bearer | Update a user |
| DELETE | `/users/{id}` | Bearer `admin` | Delete a user |

**Query filters:** `name` (like), `email` (like), `role`, `active`
**Sort by:** `id`, `name`, `level`, `sessions`, `member_since`

### Activity Records `/activity-records`

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/activity-records` | — | List activity records (paginated, filterable, sortable) |
| GET | `/activity-records/{id}` | — | Get a single activity record |
| POST | `/activity-records` | Bearer | Log a new activity record |
| DELETE | `/activity-records/{id}` | Bearer | Delete an activity record |

**Query filters:** `user_id`, `way_id`, `block_id`, `date`
**Sort by:** `id`, `date`, `user_id`

### Common query parameters

All list endpoints accept:

| Parameter | Default | Description |
|---|---|---|
| `page` | `1` | Page number |
| `per_page` | `20` | Results per page (max 100) |
| `sort` | `id` | Field to sort by |
| `order` | `asc` | Sort direction (`asc` or `desc`) |

---

## Alembic / Flask-Migrate reference

| Command | Description |
|---|---|
| `flask db init` | Initialise the migrations folder (run once) |
| `flask db migrate -m "message"` | Auto-generate a migration from model changes |
| `flask db upgrade` | Apply all pending migrations |
| `flask db downgrade` | Revert the last migration |
| `flask db history` | Show the full migration history |
| `flask db current` | Show the currently applied revision |

---

## Roles

| Role | Permissions |
|---|---|
| `admin` | Full CRUD on all resources |
| `user` | Read-only on all resources; write access requires explicit grant |
