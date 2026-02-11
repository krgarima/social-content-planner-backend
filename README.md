# Social Content Planner Backend

FastAPI backend for the Social Content Planner demo task.

## Live Links

- API Base: `https://social-content-planner-backend.onrender.com`
- API Docs (Swagger): `https://social-content-planner-backend.onrender.com/docs`
- Note: Render free tier may be slow on first load (cold start).

## Tech Stack

- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL (Supabase-compatible)
- httpx (third-party API integration)

## Features Covered

- Full CRUD REST APIs for `post_ideas`
- Dashboard summary/reporting APIs
- Third-party hashtag suggestion integration (Datamuse)

## Local Setup

1. Create and activate virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and configure values.

```bash
copy .env.example .env
```

4. Run migrations.

```bash
alembic upgrade head
```

5. Start the API server.

```bash
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

Use `./.env.example` as the template.

- `APP_NAME`
- `APP_ENV`
- `DEBUG`
- `API_PREFIX`
- `DATABASE_URL`
- `CORS_ORIGINS`
- `REQUEST_TIMEOUT_SECONDS`

Example local DB URL:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/social_content_planner
```

## Database and Migrations

- Migration files are in `alembic/versions`.
- Apply latest migration:

```bash
alembic upgrade head
```

- Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

## API Endpoints

- Health
  - `GET /health`
- CRUD
  - `POST /api/post-ideas`
  - `GET /api/post-ideas`
  - `GET /api/post-ideas/{id}`
  - `PUT /api/post-ideas/{id}`
  - `PATCH /api/post-ideas/{id}`
  - `DELETE /api/post-ideas/{id}`
- Reporting
  - `GET /api/dashboard/summary`
- Third-party integration
  - `GET /api/integrations/hashtags?q=keyword`

## Deployment Notes

- Hosting: Render
- DB: Supabase PostgreSQL
- Build command: `pip install -r requirements.txt && alembic upgrade head`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## How to Test

1. Verify health: `GET /health`
2. Create a record: `POST /api/post-ideas`
3. List records: `GET /api/post-ideas`
4. Update a record: `PATCH /api/post-ideas/{id}` or `PUT /api/post-ideas/{id}`
5. Delete a record: `DELETE /api/post-ideas/{id}`
6. Verify dashboard/report: `GET /api/dashboard/summary`
7. Verify third-party API feature: `GET /api/integrations/hashtags?q=travel`
