# FastAPI Modular Backend

Production-ready backend architecture built with FastAPI, SQLAlchemy, Alembic, and modern Python tooling.

## Tech Stack

- **Framework:** FastAPI
- **Database & ORM:** PostgreSQL / SQLite with SQLAlchemy ORM
- **Migrations:** Alembic
- **Validation & Settings:** Pydantic & Pydantic-Settings
- **Package Management:** `uv`

## Project Structure

```
backend/
├── alembic/              # Database migration scripts and versions
├── app/
│   ├── agent/            # LLM integration, RAG, and custom agent workflows
│   ├── api/              # API route endpoints and routers (v1)
│   ├── core/             # Configuration, database session, and security
│   ├── models/           # SQLAlchemy ORM database models
│   ├── schemas/          # Pydantic validation and serialization models
│   └── utils/            # Reusable helper functions and common utilities
├── tests/                # Automated test suite (pytest)
├── .env                  # Environment variables (local configuration)
├── .gitignore            # Git exclusion rules
├── .python-version       # Python runtime version pin
├── alembic.ini           # Alembic migration configuration
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation
├── uv.lock               # Locked dependency versions
└── uv.toml               # `uv` workspace and build configuration
```

## Getting Started

### Prerequisites

- Python 3.10+ installed
- `uv` package manager

### 

### Installation & Setup

1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/your-username/Habit-tracking-with-streaks.git
    cd Habit-tracking-with-streaks/backend
    ```
    
2. **Configure environment variables:**
Create a `.env` file in the backend root directory:
    
    ```
    DATABASE_URL=postgresql://user:password@host/dbname
    SECRET_KEY=your_jwt_secret_key
    OPENROUTER_API_KEY=your_openrouter_api_key
    ```
    
3. **Install dependencies and sync environment:**Bash
    
    ```bash
    uv sync
    ```
    
4. **Run database migrations:**Bash
    
    ```bash
    uv run alembic upgrade head
    ```
    
5. **Start the development server:**Bash
    
    ```bash
    uv run uvicorn main:app --reload
    ```
    
    Access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.
    
## Testing

This project features a comprehensive test suite using `pytest` and FastAPI's `TestClient` with an in-memory SQLite database (`StaticPool`) to ensure complete isolation between test functions.

### Test Architecture

- **Database Fixture (`conftest.py`):** Automatically initializes schema metadata, yields an isolated `db_session` per function, and tears down the in-memory database after completion.
- **Client Override:** Overrides FastAPI's `get_db` dependency to inject the isolated testing session.
- **Authentication Fixture:** Automatically registers and logs in a test user, returning reusable `auth_headers` with a valid Bearer token for protected route testing.

### Test Modules

- **`test_auth.py`:** Validates user registration success, duplicate email validation checks, token generation on login, and protected `/auth/me` user profile retrieval.
- **`test_habits_checkins.py`:** Tests CRUD operations for habits, authorization header validation, habit list retrieval, deletion responses, and habit check-in increments.
- **`test_streaks.py`:** Unit tests core streak calculation logic (`calculate_streaks`) across edge cases, including empty check-ins, continuous streaks, missed days, and interrupted streaks.

### Running Tests

Execute the test suite using `uv`:

```bash
uv run pytest -v
```

## 🗺️ Future Roadmap & Learning Goals

While the backend is fully functional and secure, the project will expand into a full-stack application as part of ongoing development and learning:

- **Frontend Integration (Next.js & Tailwind CSS):** Build a responsive web application utilizing the App Router to visualize habit dashboards, calendar check-in grids, and a real-time conversational chat interface with the AI coach.
- **Enhanced Analytics:** Introduce weekly and monthly habit completion rate graphs.
- **Push Notifications & Reminders:** Implement background task scheduling (e.g., Celery or FastAPI background tasks) for daily habit alerts.