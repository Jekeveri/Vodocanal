import flet as ft
from common_table import CommonTable
import src.database.bd_admin.select_server as select_server
import src.admin.admin_main as ad

def search_tab(page):
    def get_data():
        return select_server.select_task_data_all()

    def on_row_select(selected_rows):
        # Обновите видимость кнопок здесь

    def on_action(e):
        ad.add_new_tab(page, table.selected_rows)

    columns = [
        ft.DataColumn(ft.Text("ФИО")),
        ft.DataColumn(ft.Text("Адрес")),
        ft.DataColumn(ft.Text("Телефон")),
        ft.DataColumn(ft.Text("Личный счет")),
        ft.DataColumn(ft.Text("Дата")),
        ft.DataColumn(ft.Text("Статус задачи")),
        ft.DataColumn(ft.Text("Цель")),
        ft.DataColumn(ft.Text("Тип адреса")),
        ft.DataColumn(ft.Text("ID")),
    ]

    table = CommonTable(columns, get_data, on_row_select, on_action)
    return table