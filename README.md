# TecW Rocódromo API

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12-E92063?logo=pydantic&logoColor=white)
![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-6BA539?logo=openapiinitiative&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

REST API for managing a climbing gym: sport routes (vías), bouldering problems (bloques), locations (sectores), media (assets) and members (usuarios).

Built with **Flask + flask-openapi3 + SQLAlchemy + Pydantic**.

---
<img src="./banner.jpg" alt="">

---

## Table of contents

1. [Project structure](#project-structure)
2. [Setup](#setup)
3. [Running the server](#running-the-server)
4. [Interactive documentation](#interactive-documentation)
5. [Authentication](#authentication)
6. [API reference](#api-reference)
   - [Auth](#auth)
   - [Ways](#ways-apiv1ways)
   - [Blocks](#blocks-apiv1blocks)
   - [Places](#places-apiv1places)
   - [Assets](#assets-apiv1assets)
   - [Users](#users-apiv1users)
   - [Activity Records](#activity-records-apiv1activity-records)
7. [Common query parameters](#common-query-parameters)
8. [Error responses](#error-responses)
9. [Database management](#database-management)
10. [Roles and permissions](#roles-and-permissions)

---

## Project structure

```
tecw_yo/
├── tecw_02_flask/               # Phase 2 — server-rendered Jinja2 app
└── tecw_03_restful_api/         # Phase 3 — JSON REST API  ← current
    └── app/
        ├── app.py               # Application factory & entry point
        ├── db.py                # SQLAlchemy instance
        ├── auth/
        │   ├── decorators.py    # @require_auth, @require_role
        │   └── tokens.py        # JWT + refresh token logic
        ├── blueprints/          # One file per resource
        │   ├── ways.py
        │   ├── blocks.py
        │   ├── places.py
        │   ├── assets.py
        │   ├── users.py
        │   ├── activity_records.py
        │   ├── auth.py
        │   ├── query_utils.py   # Shared pagination / filter / sort helper
        │   └── response_models.py  # OpenAPI response wrappers
        ├── dtos/                # Pydantic models — validation & serialisation
        ├── models/              # SQLAlchemy ORM models
        ├── migrations/          # Alembic migrations
        ├── seeders/             # DB seed scripts
        └── fixtures/            # Raw fixture data
```

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

**3. (Optional) Set a JWT secret for production**

```bash
export JWT_SECRET="replace-with-a-long-random-string"
```

> If not set, the app falls back to an insecure dev default. Never use the default in production.

---

## Running the server

```bash
flask --app tecw_03_restful_api/app/app.py run --debug
```

Server starts at `http://127.0.0.1:5000`.

---

## Interactive documentation

The API ships with multiple documentation UIs powered by **flask-openapi3**. All of them read the same `openapi.json` spec generated automatically from the Pydantic DTOs.

| URL | UI |
|---|---|
| `http://localhost:5000/docs` | Swagger UI |
| `http://localhost:5000/docs/redoc` | Redoc |
| `http://localhost:5000/docs/rapidoc` | RapiDoc |
| `http://localhost:5000/docs/scalar` | Scalar |
| `http://localhost:5000/docs/elements` | Elements |
| `http://localhost:5000/docs/openapi.json` | Raw OpenAPI 3.1 spec |

To authorise requests from any UI, click **Authorize**, paste the `access_token` value (without the `Bearer ` prefix) and confirm. All subsequent requests will include the `Authorization: Bearer …` header automatically.

---

## Authentication

The API implements **OAuth 2.0 password grant** with short-lived JWT access tokens (15 min) and rotating opaque refresh tokens (30 days).

### Step 1 — Obtain a token pair

```http
POST /api/v1/auth/token
Content-Type: application/json
```

```json
{
  "grant_type": "password",
  "username": "admin@tecw.es",
  "password": "password"
}
```

**Response `200 OK`**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 900,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

| Field | Description |
|---|---|
| `access_token` | JWT to include in `Authorization` header |
| `token_type` | Always `Bearer` |
| `expires_in` | Seconds until the access token expires (900 = 15 min) |
| `refresh_token` | Opaque token — store securely, valid for 30 days |

### Step 2 — Authenticate requests

Add the `Authorization` header to every protected endpoint:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 3 — Refresh the token

When the access token expires (`401 Unauthorized`), obtain a new pair without re-entering credentials:

```http
POST /api/v1/auth/token
Content-Type: application/json
```

```json
{
  "grant_type": "refresh_token",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

> Each refresh token can only be used **once**. A new refresh token is returned alongside the new access token.

### Step 4 — Revoke a refresh token

Call this on logout to invalidate the stored refresh token immediately:

```http
POST /api/v1/auth/revoke
Content-Type: application/json
```

```json
{
  "token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
```

---

## API reference

Base URL: `http://localhost:5000/api/v1`

All request and response bodies are **JSON** (`Content-Type: application/json`).
List endpoints return a paginated envelope:

```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "perPage": 20,
    "total": 135,
    "totalPages": 7
  }
}
```

---

### Auth

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `POST` | `/auth/token` | — | Issue access + refresh token |
| `POST` | `/auth/revoke` | — | Revoke a refresh token |

---

### Ways `/api/v1/ways`

A **way** (vía) is a sport climbing route or top-rope route at the gym.

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/ways` | — | List ways |
| `GET` | `/ways/{id}` | — | Get a single way |
| `POST` | `/ways` | Bearer | Create a way |
| `PUT` | `/ways/{id}` | Bearer | Update a way |
| `DELETE` | `/ways/{id}` | Bearer | Delete a way |

**Filters:** `name` (partial), `grade`, `type`, `city`, `active`
**Sort fields:** `id`, `name`, `grade`, `length`, `city`

**POST / PUT body**

```json
{
  "name": "La Directa",
  "grade": "6b+",
  "type": "deportiva",
  "length": 15,
  "city": "madrid",
  "active": true,
  "description": "Classic overhanging route on the main wall.",
  "mainAssetId": 3
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `name` | string | ✔ | min 1 char |
| `grade` | string | ✔ | `3` · `4a–4c` · `5a–5c` · `6a–6c+` · `7a–7c+` · `8a–8c+` |
| `type` | string | ✔ | `deportiva` · `top-rope` · `boulder` |
| `length` | integer | ✔ | > 0 (metres) |
| `city` | string | ✔ | min 1 char |
| `active` | boolean | — | default `true` |
| `description` | string | — | optional |
| `mainAssetId` | integer | — | FK to an existing asset |

---

### Blocks `/api/v1/blocks`

A **block** (bloque) is a bouldering problem. Graded on the Hueco / V-scale.

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/blocks` | — | List blocks |
| `GET` | `/blocks/{id}` | — | Get a single block |
| `POST` | `/blocks` | Bearer | Create a block |
| `PUT` | `/blocks/{id}` | Bearer | Update a block |
| `DELETE` | `/blocks/{id}` | Bearer | Delete a block |

**Filters:** `name` (partial), `grade`, `color`, `sector`, `city`, `active`
**Sort fields:** `id`, `name`, `grade`, `height`, `city`

**POST / PUT body**

```json
{
  "name": "La Mancha",
  "grade": "V5",
  "color": "#e74c3c",
  "sector": "A1",
  "height": 4.5,
  "city": "barcelona",
  "active": true,
  "description": "Crimpy slab, bad feet.",
  "mainAssetId": null
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `name` | string | ✔ | min 1 char |
| `grade` | string | ✔ | `VB` · `V0–V16` |
| `color` | string | ✔ | hex code e.g. `#e74c3c` |
| `sector` | string | ✔ | min 1 char |
| `height` | float | ✔ | > 0 (metres) |
| `city` | string | ✔ | min 1 char |
| `active` | boolean | — | default `true` |
| `description` | string | — | optional |
| `mainAssetId` | integer | — | FK to an existing asset |

---

### Places `/api/v1/places`

A **place** (sector / ubicación) groups ways or blocks into a named location within the gym.

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/places` | — | List places |
| `GET` | `/places/{id}` | — | Get a single place |
| `POST` | `/places` | Bearer | Create a place |
| `PUT` | `/places/{id}` | Bearer | Update a place |
| `DELETE` | `/places/{id}` | Bearer | Delete a place |

**Filters:** `name` (partial)
**Sort fields:** `id`, `name`

**POST / PUT body**

```json
{
  "name": "Sala Principal",
  "description": "Main hall, routes 6a to 8b.",
  "mainAssetId": null
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `name` | string | ✔ | min 1 char |
| `description` | string | — | optional |
| `mainAssetId` | integer | — | FK to an existing asset |

---

### Assets `/api/v1/assets`

An **asset** is a media file (image or video) referenced by URL. Assets can be attached to any entity via its `mainAssetId` field.

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/assets` | — | List assets |
| `GET` | `/assets/{id}` | — | Get a single asset |
| `POST` | `/assets` | Bearer | Register an asset |
| `DELETE` | `/assets/{id}` | Bearer | Delete an asset |

**Filters:** `url` (partial)
**Sort fields:** `id`, `url`

**POST body**

```json
{
  "url": "https://cdn.tecw.es/images/la-directa.jpg"
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `url` | string | ✔ | valid HTTP/HTTPS URL |

---

### Users `/api/v1/users`

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/users` | — | List users |
| `GET` | `/users/{id}` | — | Get a single user |
| `POST` | `/users` | Bearer | Create a user |
| `PUT` | `/users/{id}` | Bearer | Update a user |
| `DELETE` | `/users/{id}` | Bearer `admin` | Delete a user |

**Filters:** `name` (partial), `email` (partial), `role`, `active`
**Sort fields:** `id`, `name`, `level`, `sessions`, `member_since`

**POST body**

```json
{
  "name": "María García",
  "email": "maria@tecw.es",
  "password": "s3cr3t!",
  "memberSince": "2024-01-15",
  "avatar": "🧗",
  "level": 3,
  "sessions": 0,
  "active": true,
  "role": "user",
  "mainAssetId": null
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `name` | string | ✔ | min 1 char |
| `email` | string | ✔ | must contain `@` |
| `password` | string | ✔ | min 6 chars (stored hashed, never returned) |
| `memberSince` | string | ✔ | date string |
| `avatar` | string | — | default `🧗` |
| `level` | integer | — | ≥ 0, default `0` |
| `sessions` | integer | — | ≥ 0, default `0` |
| `active` | boolean | — | default `true` |
| `role` | string | — | `user` · `admin`, default `user` |
| `mainAssetId` | integer | — | FK to an existing asset |

> Passwords are hashed server-side with **Werkzeug** and are never included in any response.

---

### Activity Records `/api/v1/activity-records`

An **activity record** logs a climbing session: a user completed a way or a block on a given date.

| Method | Path | Auth | Description |
|---|---|:---:|---|
| `GET` | `/activity-records` | — | List activity records |
| `GET` | `/activity-records/{id}` | — | Get a single record |
| `POST` | `/activity-records` | Bearer | Log a new record |
| `DELETE` | `/activity-records/{id}` | Bearer | Delete a record |

**Filters:** `user_id`, `way_id`, `block_id`, `date`
**Sort fields:** `id`, `date`, `user_id`

**POST body**

```json
{
  "userId": 1,
  "wayId": 12,
  "blockId": null,
  "notes": "Flash! Tried the left-hand variant.",
  "mainAssetId": null
}
```

| Field | Type | Required | Constraints |
|---|---|:---:|---|
| `userId` | integer | ✔ | > 0, must exist |
| `wayId` | integer | — | > 0; provide either `wayId` or `blockId` |
| `blockId` | integer | — | > 0; provide either `wayId` or `blockId` |
| `notes` | string | — | optional free text |
| `mainAssetId` | integer | — | FK to an existing asset |

> The `date` field is set automatically to the current server date and is not accepted in the request body.

---

## Common query parameters

All `GET /resource` list endpoints accept:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | `1` | Page number (1-based) |
| `per_page` | integer | `20` | Results per page (max 100) |
| `sort` | string | `id` | Field to sort by (see each resource) |
| `order` | string | `asc` | `asc` or `desc` |
| `<filter_field>` | string | — | Resource-specific filter (see each resource) |

**Example — ways paginated, filtered and sorted:**

```
GET /api/v1/ways?page=2&per_page=10&sort=grade&order=desc&city=madrid&active=true
```

---

## Error responses

All errors return a JSON body with at least an `error` field.

| Status | When |
|---|---|
| `400 Bad Request` | Malformed JSON or unsupported grant type |
| `401 Unauthorized` | Missing, invalid or expired access token |
| `403 Forbidden` | Valid token but insufficient role |
| `404 Not Found` | Resource does not exist |
| `422 Unprocessable Entity` | Pydantic validation failed — body includes a `details` array |
| `500 Internal Server Error` | Unexpected server error |

**Example 422 response**

```json
{
  "error": "Validation failed",
  "details": [
    {
      "type": "value_error",
      "loc": ["grade"],
      "msg": "Value error, grade must be one of: 3, 4a, 4b ...",
      "input": "9z"
    }
  ]
}
```

---

## Database management

All commands require `--app tecw_03_restful_api/app/app.py`.

**Apply migrations**

```bash
flask --app tecw_03_restful_api/app/app.py db upgrade
```

**Seed initial data**

```bash
flask --app tecw_03_restful_api/app/app.py seed
```

> Default admin account: `admin@tecw.es` / `password`

**Reset database** (dev only — drops all data)

```bash
flask --app tecw_03_restful_api/app/app.py reset-db
flask --app tecw_03_restful_api/app/app.py db upgrade
flask --app tecw_03_restful_api/app/app.py seed
```

### Alembic reference

| Command | Description |
|---|---|
| `flask db init` | Initialise migrations folder (run once) |
| `flask db migrate -m "msg"` | Generate migration from model changes |
| `flask db upgrade` | Apply all pending migrations |
| `flask db downgrade` | Revert the last migration |
| `flask db downgrade base` | Revert all migrations |
| `flask db history` | Show full migration history |
| `flask db current` | Show currently applied revision |

---

## Roles and permissions

| Role | Permissions |
|---|---|
| *(unauthenticated)* | Read all resources (`GET`) |
| `user` | Read all + write ways, blocks, places, assets and activity records |
| `admin` | Full access including user deletion |