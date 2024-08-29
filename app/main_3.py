from fastapi import FastAPI, Cookie, Response, Header, Request, HTTPException
from typing import List

from app.models.User import User
from app.models.Feedback import Feedback
from app.models.UserCreate import UserCreate
from app.models.Product import Product
from app.models.UserAuth import UserAuth

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


# имитируем хранилище юзеров
sample_user: dict = {"username": "user123", "password": "password123"}  # создали тестового юзера, якобы он уже
# зарегистрирован у нас
fake_db: list[UserAuth] = [UserAuth(**sample_user)]  # имитируем базу данных
# имитируем хранилище сессий
sessions: dict = {}  # это можно хранить в кэше, например в Redis


# основная логика программы
@app.post("/login")
async def login(user: UserAuth, response: Response):
    for person in fake_db:  # перебрали юзеров в нашем примере базы данных
        if person.username == user.username and person.password == user.password:  # сверили логин и пароль
            session_token = "abc123xyz456"  # тут можно использовать модуль uuid (в продакшене), или модуль random
            # (для выполнения задания), или самому написать рандомное значение куки, т.к. это пример тестовый
            sessions[session_token] = user  # сохранили у себя в словаре сессию, где токен - это ключ, а значение -
            # объект юзера
            response.set_cookie(key="session_token", value=session_token, httponly=True)  # тут установили куки с
            # защищенным флагом httponly - недоступны для вредоносного JS; флаг secure означает, что куки идут только
            # по HTTPS
            return {"message": "Куки установлены"}
    return {"message": "Invalid username or password"}  # тут можно вернуть что хотите, в ТЗ не конкретизировалось,
    # что делать, если логин/пароль неправильные


@app.get("/user")
async def user_info(session_token=Cookie()):
    user = sessions.get(session_token)  # ищем в сессиях был ли такой токен создан, и если был, то возвращаем
    # связанного с ним юзера
    if user:
        return user.dict()  # у pydantic моделей есть метод dict(), который делает словарь из модели. Можно сразу
        # хранить словарь в сессии, не суть. Для Pydantic версии > 2 метод переименован в model_dump()
    return {"message": "Unauthorized"}


@app.get("/headers")
async def headers_def(user_aget: str | None = Header(), accept_language: str | None = Header()):
    if user_aget and accept_language:
        return {
            "User-agent": user_aget,
            "Accept-Language": accept_language
        }
    return HTTPException(status_code=400, detail="Headers User-agent or Accept-Language not found")
