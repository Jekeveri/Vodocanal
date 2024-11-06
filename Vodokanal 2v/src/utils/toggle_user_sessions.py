import os
from datetime import datetime, timedelta
import jwt
from src.database.bd_users import bd_server_user, local
from src.database.bd_admin import local as admin_local
from src.utils.func import show_snack_bar
from src.utils.navigations import role_definition
from src.utils.verifications import authentication

SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")  # Используйте переменную окружения для секретного ключа
TOKEN_EXPIRATION = timedelta(hours=1)  # Токен действителен 1 час

def create_token(user_data):
    expiration = datetime.utcnow() + TOKEN_EXPIRATION
    token = jwt.encode({
        'user_id': user_data['id'],
        'login': user_data['login'],
        'privileges': user_data['privileges'],
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def handle_user_sessions(page):
    token = page.client_storage.get("user_token")
    if token:
        user_data = verify_token(token)
        if user_data:
            role_definition(user_data['privileges'], page)
            show_snack_bar(page, "Сессия восстановлена.")
            return

    if os.path.exists("database_client.db"):
        user_data = local.select_bd.select_user_data() or admin_local.select_user_data()
        if user_data:
            login, password, privileges = user_data[0][1:4]
            if login and password:
                # Здесь должна быть проверка учетных данных на сервере
                server_verified = bd_server_user.verify_credentials(login, password)
                if server_verified:
                    token = create_token({'id': user_data[0][0], 'login': login, 'privileges': privileges})
                    page.client_storage.set("user_token", token)
                    role_definition(privileges, page)
                    show_snack_bar(page, "Успешный вход в систему.")
                else:
                    authentication(page)
            else:
                authentication(page)
        else:
            authentication(page)
    else:
        authentication(page)