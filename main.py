
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Base, engine, SessionLocal
from models import UserPlan
from ai_service import generate_plan, generate_nutrition_tip

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FitBuddy AI Fitness Planner")

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None}
    )


@app.post("/generate", response_class=HTMLResponse)
def create_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    goal: str = Form(...),
    level: str = Form(...),
    days: int = Form(...)
):
    name = name.strip()

    if not name or not 13 <= age <= 100 or not 1 <= days <= 7:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Please enter valid details."},
            status_code=400
        )

    try:
        plan = generate_plan(name, age, goal, level, days)
        tip = generate_nutrition_tip(goal)

        with SessionLocal() as db:
            saved = UserPlan(
                name=name,
                age=age,
                goal=goal,
                level=level,
                days=days,
                plan=plan,
                nutrition_tip=tip
            )
            db.add(saved)
            db.commit()

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "name": name,
                "plan": plan,
                "nutrition_tip": tip
            }
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"Could not generate plan: {exc}"
            },
            status_code=500
        )


@app.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    with SessionLocal() as db:
        users = db.query(UserPlan).order_by(
            UserPlan.id.desc()
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={"users": users}
        )


@app.get("/api/users")
def api_users():
    with SessionLocal() as db:
        users = db.query(UserPlan).order_by(
            UserPlan.id.desc()
        ).all()

        return [
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "goal": user.goal,
                "level": user.level,
                "days": user.days,
                "plan": user.plan,
                "nutrition_tip": user.nutrition_tip
            }
            for user in users
        ]


@app.get("/health")
def health():
    return {"status": "ok"}
