# FitBuddy - Project Workflow

This document maps the application to the Epic/Story structure in the project requirement.

## Pre-Requisites

- Python 3.10 or newer
- VS Code
- Internet connection for real Gemini mode
- Google Gemini API key for real AI generation

## Project Workflow

```text
User
  ↓
Jinja2 Frontend
  ↓
FastAPI Routes
  ↓
Pydantic Validation
  ↓
AI Layer ─────→ Google Gemini
  ↓
Workout / Nutrition / Updated Plan
  ↓
SQLite + SQLAlchemy
  ↓
Jinja2 Result Page
```

## Epic 1: Model selection and Architecture

### Story 1: Research and Select the Appropriate Generative AI Model

FitBuddy uses Google's Gemini Generative AI model through the `google-genai` SDK. The model is configurable through `.env`. The default configured model is `gemini-2.5-flash`.

### Story 2: Define the architecture of the application

- `app/main.py` - FastAPI application entry point
- `app/routes.py` - frontend and API routing
- `app/schemas.py` - request validation
- `app/database.py` - SQLite/SQLAlchemy persistence
- `app/ai/` - Gemini client and generation logic
- `templates/` - Jinja2 frontend
- `static/` - CSS

### Story 3: Set up the development environment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Epic 2: Core functionalities Development

### Story 1: Develop the core functionalities

Implemented:

1. User fitness profile collection
2. Personalized 7-day workout generation
3. AI nutrition guidance
4. User feedback collection
5. AI updated workout plan
6. SQLite persistence

### Story 2: Implement the FastAPI Backend

Important routes:

- `POST /generate-workout`
- `POST /submit-feedback`
- `GET /view-all-users`
- `POST /api/generate-workout`
- `POST /api/submit-feedback`
- `GET /api/users`
- `GET /health`

## Epic 3: App.py Development

`app/main.py` creates the FastAPI application, mounts static files, initializes database tables on startup, registers routes, and exposes `/health`.

Run command:

```powershell
uvicorn app.main:app --reload
```

## Epic 4: Frontend Development

### Story 1: Designing and Developing User Interface

- `templates/index.html` - user input form
- `templates/result.html` - generated plan and feedback UI
- `templates/all_users.html` - admin view
- `static/style.css` - responsive UI

### Story 2: Creating Dynamic Templates with FastAPI's Jinja2

The templates receive dynamic values such as:

```text
{{ user.username }}
{{ workout_plan }}
{{ nutrition_tip }}
{{ updated_plan }}
```

## Epic 5: Deployment

### Story 1: Preparing the Application for Local Deployment

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Story 2: Testing and Verifying Local Deployment

Open:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`

Automated tests:

```powershell
pytest
```

## Conclusion

FitBuddy combines a FastAPI backend, Jinja2 frontend, SQLite database and Generative AI layer to create personalized fitness plans. The modular structure makes the AI, API, database and UI components easy to test and extend.
