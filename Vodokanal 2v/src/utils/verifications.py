import flet as ft
import asyncio
import bcrypt
from src.database import auth
from src.utils.func import show_snack_bar

async def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

async def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def authentication(page: ft.Page):
    page.clean()
    page.navigation_bar = None
    page.appbar = None
    page.controls.clear()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    login = ft.TextField(label="Логин", width=page.width * 0.90)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=page.width * 0.90)

    async def on_click(e):
        if login.value and password.value:
            # Здесь должна быть асинхронная функция проверки учетных данных
            user = await auth.check_user_credentials(login.value, password.value)
            if user:
                hashed_password = await hash_password(password.value)
                if await check_password(password.value, hashed_password):
                    # Успешная аутентификация
                    show_snack_bar(page, "Успешный вход в систему.")
                    # Здесь должен быть код для перехода на главную страницу
                else:
                    show_snack_bar(page, "Неправильный логин или пароль.")
            else:
                show_snack_bar(page, "Пользователь не найден.")
        else:
            show_snack_bar(page, "Пожалуйста, заполните все поля.")

    login_button = ft.ElevatedButton(text="Вход", on_click=lambda _: asyncio.create_task(on_click(_)))

    page.add(
        ft.Row(
            [
                ft.Column(
                    [login, password, login_button],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()