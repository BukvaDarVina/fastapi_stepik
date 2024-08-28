from fastapi import FastAPI
from app.models.User import User
from app.models.Feedback import Feedback
from app.models.UserCreate import UserCreate


app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

fake_feedback = []

fake_users_2: list[UserCreate] = []


@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.get("/users/")
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])


@app.post("/feedback")
async def post_feedback(feedback: Feedback):
    fake_feedback.append({'name': feedback.name, 'message': feedback.message})
    return {'message': f'Feedback received. Thank you, {feedback.name}'}


@app.get("/feedbacks")
async def show_feedback(limit: int = 10):
    if len(fake_feedback) > 0:
        print(fake_feedback)
        return dict(list(fake_feedback[:limit]))
    return {"error": "Feedbacks not found"}


@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    fake_users_2.append(user)
    return user


@app.get("/show_user")
async def show_users():
    return {"users": fake_users_2}
