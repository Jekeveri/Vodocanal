import flet as ft
import src.utils.toggle_user_sessions


def main(page: ft.Page):
    page.theme_mode = 'light'
    page.title = "Мобильный контралер"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    src.utils.toggle_user_sessions.handle_user_sessions(page)


ft.app(target=main)
