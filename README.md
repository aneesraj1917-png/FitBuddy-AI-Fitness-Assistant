# FitBuddy - Generative AI Fitness Plan Generator

AI-powered personalized fitness assistant using FastAPI and Gemini AI.

Complete FastAPI + Jinja2 + SQLite + Google Gemini project matching the Epic/Story workflow.

## 1. Open in VS Code

Extract the ZIP and open the `FitBuddy` folder in VS Code.

## 2. Install

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Run locally

The included `.env` uses `AI_DEMO_MODE=true`, so the project can be tested without a Gemini key.

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## 4. Real Gemini AI

Edit `.env`:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
AI_DEMO_MODE=false
```

Restart Uvicorn.

## 5. Test

```powershell
pytest
```

Swagger: `http://127.0.0.1:8000/docs`

Health: `http://127.0.0.1:8000/health`

Admin: `http://127.0.0.1:8000/view-all-users`

Default demo admin token: `fitbuddy-admin`

## Folder Structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   └── ai/
│       ├── __init__.py
│       ├── gemini_client.py
│       ├── gemini_generator.py
│       ├── gemini_flash_generator.py
│       └── updated_plan.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
├── static/
│   └── style.css
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── PROJECT_WORKFLOW.md
└── README.md
```
