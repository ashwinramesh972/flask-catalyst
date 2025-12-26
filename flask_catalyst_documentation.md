# flask-catalyst Documentation Built by Ashwin

flask-catalyst is a production-ready Flask backend boilerplate designed for scalability, flexibility, and ease of use. It supports modern features like JWT authentication, role-based permissions, file uploads with multiple storage options, pagination, logging, rate limiting, and email sending. It's Dockerized for one-command deployment and can integrate with any frontend.

This documentation is written for beginners and experienced developers alike. If you're new, it explains how everything works step by step. If you're advanced, it shows how to extend it.

---

## Folder Structure

Here's the complete folder structure of flask-catalyst. Each folder and file has a specific purpose, explained in the next sections.

### Complete Folder Tree

```text
flask-catalyst/
├── app/                     # Core application code (main Flask app)
│   ├── __init__.py          # App factory: creates the Flask app, initializes extensions, registers blueprints
│   ├── api/                 # All API routes (endpoints for your app)
│   │   ├── __init__.py      # Registers all API blueprints
│   │   ├── auth.py          # Authentication routes (register, login)
│   │   ├── admin.py         # Admin-only routes (e.g., user management)
│   │   └── files.py         # File upload routes
│   ├── core/                # Core configurations and extensions
│   │   ├── __init__.py      # (Optional) Empty or for future core utils
│   │   ├── config.py        # App configurations (dev/prod, database URLs)
│   │   └── extensions.py    # Global extensions like db, jwt (if not in __init__.py)
│   ├── models/              # Database models (SQLAlchemy classes)
│   │   ├── __init__.py      # Imports all models for migrations
│   │   └── user.py          # User model (with roles, password hashing)
│   ├── schemas/             # Data schemas (Pydantic for validation/response)
│   │   ├── __init__.py      # (Optional) Imports all schemas
│   │   └── user.py          # User schemas for input/output
│   ├── services/            # Business logic services (e.g., user service for complex operations)
│   │   ├── __init__.py      # (Optional) Imports all services
│   │   └── user_service.py  # Example service for user operations
│   └── utils/               # Reusable helpers (the "tools" of your app)
│       ├── __init__.py      # (Optional) Imports all utils
│       ├── error_handler.py # Global error handlers for JSON responses
│       ├── file_upload.py   # File upload helper (local, Cloudinary, S3)
│       ├── logger.py        # Logging setup with daily rotation
│       ├── middleware.py    # Request middleware (timing, user tracking)
│       ├── pagination.py    # Pagination helper for queries
│       ├── permissions.py   # Role-based permission decorators
│       ├── rate_limiter.py  # Rate limiting to prevent abuse
│       ├── response.py      # Standard success/error JSON responses
│       └── email.py         # Email sending helper
├── migrations/              # Database migrations (Alembic files — auto-generated)
├── tests/                   # Unit/integration tests (pytest)
│   ├── __init__.py          # (Optional) Test setup
│   ├── test_auth.py         # Tests for auth routes
│   ├── test_admin.py        # Tests for admin routes
│   └── test_utils.py        # Tests for utils
├── instance/                # Instance-specific files (gitignore'd)
│   ├── app.db               # SQLite database (for local dev)
│   └── uploads/             # Local file uploads folder
├── requirements/            # Requirements files
│   ├── base.txt             # Core dependencies
│   ├── development.txt      # Dev tools (testing, linting)
│   └── production.txt       # Prod-only (gunicorn)
├── frontend-examples/       # Examples for frontend integration
│   ├── react-js/            # React JS example code
│   ├── react-typescript/    # React TS example
│   ├── vue-3/               # Vue 3 example
│   └── nextjs/              # Next.js example
├── .env.example             # Template for environment variables
├── .gitignore               # Files to ignore in Git
├── docker-compose.yml       # Docker setup for local/prod
├── Dockerfile               # Docker image for backend
├── main.py                  # Entry point to run the app
└── README.md                # This documentation file
```

---

## How the Boilerplate Works (For Beginners)

flask-catalyst uses the app factory pattern (in app/__init__.py). This means you don't create the Flask app in one file — you use a function create_app() that sets up everything (config, DB, routes) based on environment (dev/prod).

### Basic Workflow

- Start the app: `python main.py` (or `docker compose up`)
- Run migrations: `flask db migrate` + `flask db upgrade`
- Test endpoints: Use curl or Postman (e.g., POST to `/api/auth/register`)

### If you're a total beginner:

- Install: `pip install -r requirements/base.txt`
- Run: `python main.py`
- Add new things: Follow the "How to Add X" sections below

---

## Explanation of Each Folder and File

### app/ — Core Application Code

This is the heart of your Flask app. All your custom code goes here.

#### __init__.py

- The "factory" file. Creates the Flask app, loads config, initializes extensions (DB, JWT, CORS), registers blueprints (API routes), and sets up middlewares (logging, rate limiting).
- Why? Allows different configs for dev/prod.
- How it works: `create_app("development")` loads `config_by_name["development"]` and sets up everything.
- How to add something: Import your new utility here and call it (e.g., `setup_my_new_util(app)`).

#### api/ — API Routes

- All API endpoints (routes).
- Why? Keeps routes organized (one file per feature, e.g., auth.py, admin.py).
- How it works: Each file defines a Blueprint (mini-app) with routes. __init__.py imports them.
- How to add a new route: Create `api/my_feature.py` with `@api_bp.route("/my-feature")`, import in __init__.py.

#### core/ — Configurations and Extensions

- Why? Keeps setup clean (config.py for env vars, extensions.py for DB/JWT).
- How it works: config.py loads from .env or defaults. Extensions are global.
- How to add: Put new config vars in config.py (e.g., `MY_NEW_VAR = os.getenv("MY_NEW_VAR")`).

#### models/ — Database Models

- Database models (SQLAlchemy classes).
- Why? Defines your data (e.g., User table with role, password).
- How it works: Each file (e.g., user.py) defines a class like `User(db.Model)`. __init__.py imports all for migrations.
- How to add a new model: Create `models/my_model.py` with `class MyModel(db.Model):`, import in __init__.py, then run `flask db migrate`.

#### schemas/ — Data Schemas

- Data validation/response schemas (Pydantic).
- Why? Ensures clean input/output (e.g., UserOut for JSON).
- How it works: user.py defines classes like `UserOut(BaseModel)`. Use in routes: `UserOut.from_orm(user).dict()`.
- How to add: Create `schemas/my_schema.py` with `class MySchema(BaseModel):`, import in routes.

#### services/ — Business Logic

- Business logic services (e.g., complex operations).
- Why? Keeps routes simple — services handle logic (e.g., `user_service.create_user()`).
- How it works: Each file (e.g., user_service.py) has functions. Routes call them.
- How to add: Create `services/my_service.py` with functions, import in routes.

#### utils/ — Reusable Helpers

- Reusable helpers (the "tools" kit).
- Why? Avoid duplicate code (e.g., response.py for JSON, file_upload.py for uploads).
- How it works: Each file is a tool. Import in __init__.py or routes.
- How to add a new helper: Create `utils/my_helper.py` with functions/classes, import in __init__.py if global (e.g., `setup_my_helper(app)`), or directly in routes.

---

## migrations/ — Database Changes

- Why? Tracks schema changes (e.g., add column).
- How it works: Run `flask db migrate` to generate, `flask db upgrade` to apply.
- How to add: Make model change → run migrate/upgrade.

---

## tests/ — Tests

- Why? Ensures your app doesn't break (pytest).
- How it works: Run `pytest`. Each file tests one part (e.g., test_auth.py).
- How to add: Create `tests/test_my_feature.py` with `@pytest.mark.app` tests.

---

## instance/ — Instance-specific Files

- Why? Stores DB + uploads (gitignore'd).
- How it works: Auto-created. Never commit.
- How to add: No need — it's for runtime files.

---

## requirements/ — Dependencies

- Why? Separate base/dev/prod.
- How it works: `pip install -r requirements/base.txt`.
- How to add: Add to base.txt, run pip install.

---

## frontend-examples/ — Frontend Connection Examples

- Why? Shows how to connect any frontend.
- How it works: Copy-paste code from here to your frontend.
- How to add: Create new folder (e.g., angular/) with connection code.

---

## .env.example — Environment Variables Template

- Why? Shows users what to set in .env (secrets, config).
- How it works: Copy to .env and fill.
- How to add: Add new vars as needed.

---

## .gitignore — Ignore Files

- Why? Keeps Git clean (no venv, no .env secrets).
- How it works: Git ignores listed files.
- How to add: Add new patterns (e.g., `*.temp`).

---

## docker-compose.yml + Dockerfile — Deployment

- Why? One command run.
- How it works: `docker compose up` starts backend + DB.
- How to add: Add services (e.g., redis for cache).

---

## main.py — Entry Point

- Why? Runs the app (like Django manage.py).
- How it works: `python main.py` starts server.
- How to add: No need — it's the launcher.

---

## How Each Helper Works (Detailed Explanation)

All helpers are in `app/utils/`. They are reusable “tools” to avoid duplicate code. To use:

- Import in __init__.py if global (e.g., `setup_logger(app)`)
- Call in routes/models as needed

### response.py — JSON Responses

- Why created? Every API needs consistent success/error JSON. This avoids manual jsonify() everywhere.
- Purpose: Standardize API outputs, make code clean.
- How it works: `success(data, message, status)` returns JSON + code.
- How to use: In route: `return success(user.to_dict(), "User fetched")`
- How to add similar: Create new function for custom formats.

### error_handler.py — Global Errors

- Why? Handles 400/401/404/500 automatically as JSON.
- Purpose: User-friendly errors, no ugly stack traces.
- How it works: Registers `@app.errorhandler` for codes/exceptions.
- How to use: Called automatically on errors.
- How to add: Add new `@app.errorhandler(MyError)` in the file.

### pagination.py — Query Pagination

- Why? Lists (users, posts) need page/per_page/total. This makes it one line.
- Purpose: Efficient data fetching, avoids loading 1000+ items.
- How it works: Takes query + schema → returns paginated JSON.
- How to use: `return paginate(User.query, user_schema)`
- How to add: Extend for sorting/filtering.

### permissions.py — Role Permissions

- Why? Protect routes (admin-only).
- Purpose: Security — prevent users from accessing admin features.
- How it works: `@admin_required` decorator checks JWT role.
- How to use: `@admin_required` above route.
- How to add: Create `@super_admin_required` for more roles.

### file_upload.py — File Uploads

- Why? Handle images/PDFs with local/cloud options.
- Purpose: Flexible storage for profiles, documents.
- How it works: Uploads to local/Cloudinary/S3 based on .env.
- How to use: `url = upload_file(request.files['file'])`
- How to add: Add Google Cloud option.

### logger.py + middleware.py — Logging

- Why? Track requests with user/IP/duration.
- Purpose: Debug, monitor, security audits.
- How it works: Logs every request in beautiful format.
- How to use: Automatic — `app.logger.info("msg")`.
- How to add: Add Slack/email for errors.

### rate_limiter.py — Rate Limiting

- Why? Prevent brute force attacks.
- Purpose: Security — limit login attempts.
- How it works: `@limiter.limit("5 per minute")` on routes.
- How to use: Add to sensitive routes like login.
- How to add: Add per-IP limits.

### email.py — Email Sending

- Why? For verification/reset.
- Purpose: Real apps need emails.
- How it works: Send with HTML templates.
- How to use: `send_email(to, subject, html)`
- How to add: Add templates with Jinja.

---

## How to Add New Things (Beginner Guide)

### Add a New Helper (e.g., my_helper.py)

1. Create `app/utils/my_helper.py` with functions.
2. Import and call in __init__.py (e.g., `setup_my_helper(app)`).
3. Use in routes: `from ..utils.my_helper import my_function`.
4. Test: Run app, check logs.

### Add a New Model (e.g., post.py)

1. Create `app/models/post.py` with `class Post(db.Model):`.
2. Import in `app/models/__init__.py`: `from .post import Post`.
3. Run `flask db migrate` + `flask db upgrade`.
4. Add routes to use it.

### Add a New Route (e.g., blog.py)

1. Create `app/api/blog.py` with `@api_bp.route("/blog")`.
2. Import in `app/api/__init__.py`: `from .blog import *`.
3. Add permissions if needed.

### Add a New Schema (e.g., post.py)

1. Create `app/schemas/post.py` with `class PostOut(BaseModel):`.
2. Use in routes: `PostOut.from_orm(post).dict()`.

### Add a New Service (e.g., blog_service.py)

1. Create `app/services/blog_service.py` with functions.
2. Call in routes: `from ..services.blog_service import create_blog`.

