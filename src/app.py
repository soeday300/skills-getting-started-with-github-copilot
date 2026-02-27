"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
import os

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # スポーツ関連
    "Soccer": {
        "description": "Outdoor team sport played on a field",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Volleyball": {
        "description": "Indoor team sport, three sets to win",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": []
    },
    # 芸術関連
    "Painting": {
        "description": "Express yourself with color and canvas",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama": {
        "description": "Acting and stage production workshop",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Sculpture": {
        "description": "Carve and mold three‑dimensional art",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 12,
        "participants": []
    },
    "Photography": {
        "description": "Learn to shoot and edit photographs",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    # 知的活動
    "Book Club": {
        "description": "Discuss a new book each month",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Math Club": {
        "description": "Solve puzzles and compete in math contests",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # 重複登録チェック
    if email in activity["participants"]:
        raise HTTPException(status_code=400,
                            detail=f"{email} is already signed up for {activity_name}")

    # 定員チェック
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400,
                            detail=f"{activity_name} is full")

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404,
                            detail=f"{email} is not registered for {activity_name}")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
