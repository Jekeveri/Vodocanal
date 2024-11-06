import os
import flet as ft
import psycopg2
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def get_user_db_connection(login, password):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("DBNAME", "Vodocanal"),
            user=login,
            password=password,
            host=os.environ.get("HOST", "45.151.31.154"),
            port=os.environ.get("PORT", "5432")
        )
        yield conn
    except Exception as ex:
        logger.error(f"Database connection error: {ex}")
        yield None
    finally:
        if conn:
            conn.close()

def show_snack_bar(page: ft.Page, message: str):
    snack_bar = ft.SnackBar(
        content=ft.Text(message),
        open=True,
        duration=800
    )
    page.overlay.append(snack_bar)
    page.update()

def show_alert_yn(page: ft.Page, message: str):
    def on_button_click(e):
        page.close(bs)

    bs = ft.AlertDialog(
        modal=True,
        title=ft.Text("Предупреждение"),
        content=ft.Text(message),
        actions=[
            ft.ElevatedButton("Да", on_click=on_button_click),
            ft.ElevatedButton("Назад", on_click=on_button_click)
        ],
    )
    page.open(bs)
    page.update()