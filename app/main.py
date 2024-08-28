from fastapi import FastAPI
from typing import List

from app.models.User import User
from app.models.Feedback import Feedback
from app.models.UserCreate import UserCreate
from app.models.Product import Product


app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}

fake_feedback = []

fake_users_2: list[UserCreate] = []

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


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


@app.get("/product/{product_id}")
async def read_product(product_id: int) -> Product:
    product = [item for item in sample_products if item['product_id'] == product_id]
    if product:
        return product[0]
    # return {"error": f"product with id {product_id} not found"}


@app.get("/products/search")
async def search(keyword: str, category: str = None, limit: int = 10):
    result = list(filter(lambda item: keyword.lower() in item['name'].lower(), sample_products))

    if category:
        result = list(filter(lambda item: item['category'] == category, result))

    return {"products": result[:limit]}

