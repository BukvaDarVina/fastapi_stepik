import jwt

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = "mysecretkey"  # тут мы в реальной практике используем что-нибудь вроде команды Bash (Linux)
# 'openssl rand -hex 32', и храним очень защищено
ALGORITHM = "HS256"  # плюс в реальной жизни мы устанавливаем "время жизни" токена

# Пример информации из БД
USER_DATA = [
    {"username": "admin", "password": "adminpass"}
]  # в реальной БД мы храним только ХЭШИ паролей (можете прочитать про библиотеку, к примеру, 'passlib') +
# + соль (известная только нам добавка к паролю)


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)  # кодируем токен, передавая в него наш словарь с тем,
    # что мы хотим там разместить


# Функция получения User'а по токену
def get_user_from_token(token: str):
    try:
        payloard = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # декодируем токен
        return payloard.get("sub")  # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере
        # (subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания'
        # и другое, что мы сами туда кладем
    except jwt.ExpiredSignatureError:
        pass  # тут какая-то логика ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        pass  # тут какая-то логика обработки ошибки декодирования токена


# Функция для получения пользовательских данных на основе имени пользователя
def get_user(username: str):
    for user in USER_DATA:
        if user.get("username") == username:
            return user
    return None


# закодируем токен, внеся в него словарь с утверждением о пользователе
token = create_jwt_token({"sub": "admin"})

print(token)  # можете посмотреть как выглядит токен jwt

# декодируем токен и излечен из него информацию о юзере, которую мы туда зашили
username = get_user_from_token(token)

print(username)  # посмотрим, что возвращается то, что ожидаем

# и теперь пойдем в нашу базу данных искать такого юзера по юзернейму
current_user = get_user(username)

print(current_user)  # удостоверимся, что нашелся тот, кто нужен
