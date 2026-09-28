from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db, User
from .schemas import UserInput, FeedbackInput
from .ai.gemini_generator import generate_workout
from .ai.gemini_flash_generator import generate_nutrition_tip
from .ai.updated_plan import update_plan


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

router = APIRouter()


def find_user(db: Session, user_id: str):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME
        }
    )


# --------------------------------------------------
# GENERATE WORKOUT - WEB
# --------------------------------------------------

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_page(
    request: Request,

    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = UserInput(
            username=username.strip(),
            user_id=user_id.strip(),
            age=age,
            weight=weight,
            goal=goal.strip(),
            intensity=intensity.lower()
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "error": f"Invalid input: {exc}",
                "user": None,
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None
            },
            status_code=400
        )

    # Check duplicate user
    if find_user(db, data.user_id):

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "error": "User ID already exists. Please use another User ID.",
                "user": None,
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None
            },
            status_code=400
        )

    # Create user
    user = User(
        username=data.username,
        user_id=data.user_id,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    try:

        # Generate workout
        plan = generate_workout(
            data.username,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        # Generate nutrition recommendation
        nutrition = generate_nutrition_tip(
            data.goal
        )

        user.workout_plan = plan
        user.nutrition_tip = nutrition

        db.commit()
        db.refresh(user)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "error": None,
                "user": user,
                "workout_plan": plan,
                "nutrition_tip": nutrition,
                "updated_plan": None
            }
        )

    except Exception as exc:

        db.delete(user)
        db.commit()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "error": str(exc),
                "user": None,
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None
            },
            status_code=500
        )


# --------------------------------------------------
# FEEDBACK - WEB
# --------------------------------------------------

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_page(
    request: Request,

    user_id: str = Form(...),
    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    user = find_user(db, user_id)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if not user.workout_plan:

        raise HTTPException(
            status_code=400,
            detail="Workout plan not found."
        )

    updated = update_plan(
        user.workout_plan,
        feedback,
        user.username,
        user.age,
        user.weight,
        user.goal,
        user.intensity
    )

    user.feedback = feedback
    user.updated_plan = updated

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "error": None,
            "user": user,
            "workout_plan": user.workout_plan,
            "nutrition_tip": user.nutrition_tip,
            "updated_plan": updated
        }
    )


# --------------------------------------------------
# ADMIN USERS
# --------------------------------------------------

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    token: str = "",
    db: Session = Depends(get_db)
):

    authenticated = token == settings.ADMIN_TOKEN

    users = (
        db.query(User)
        .order_by(User.id.desc())
        .all()
        if authenticated
        else []
    )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "authenticated": authenticated,
            "users": users,
            "token": token
        }
    )


# --------------------------------------------------
# DELETE USER
# --------------------------------------------------

@router.post("/admin/delete/{user_id}")
def admin_delete_user(
    user_id: str,

    token: str = Form(...),

    db: Session = Depends(get_db)
):

    if token != settings.ADMIN_TOKEN:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin token."
        )

    user = find_user(db, user_id)

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    db.delete(user)
    db.commit()

    return RedirectResponse(
        url=f"/view-all-users?token={token}",
        status_code=303
    )


# --------------------------------------------------
# API - GENERATE WORKOUT
# --------------------------------------------------

@router.post("/api/generate-workout")
def api_generate_workout(
    data: UserInput,
    db: Session = Depends(get_db)
):

    if find_user(db, data.user_id):

        raise HTTPException(
            status_code=400,
            detail="User ID already exists."
        )

    user = User(
        username=data.username,
        user_id=data.user_id,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    try:

        plan = generate_workout(
            data.username,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        nutrition = generate_nutrition_tip(
            data.goal
        )

        user.workout_plan = plan
        user.nutrition_tip = nutrition

        db.commit()

        return {
            "success": True,
            "user_id": user.user_id,
            "workout_plan": plan,
            "nutrition_tip": nutrition
        }

    except Exception as exc:

        db.delete(user)
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# --------------------------------------------------
# API - FEEDBACK
# --------------------------------------------------

@router.post("/api/submit-feedback")
def api_submit_feedback(
    data: FeedbackInput,
    db: Session = Depends(get_db)
):

    user = find_user(
        db,
        data.user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    updated = update_plan(
        user.workout_plan,
        data.feedback,
        user.username,
        user.age,
        user.weight,
        user.goal,
        user.intensity
    )

    user.feedback = data.feedback
    user.updated_plan = updated

    db.commit()

    return {
        "success": True,
        "user_id": user.user_id,
        "updated_plan": updated
    }


# --------------------------------------------------
# API - ALL USERS
# --------------------------------------------------

@router.get("/api/users")
def api_users(
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )

    return [
        {
            "id": user.id,
            "username": user.username,
            "user_id": user.user_id,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "workout_plan": user.workout_plan,
            "nutrition_tip": user.nutrition_tip,
            "feedback": user.feedback,
            "updated_plan": user.updated_plan
        }
        for user in users
    ]