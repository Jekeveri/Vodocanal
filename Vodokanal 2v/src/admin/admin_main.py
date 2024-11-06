import flet as ft
from src.admin.screens.home_tab import home_tab
from src.admin.screens.search_tab import search_tab
from src.admin.screens.assignment_tab import assignment_tab
from src.admin.screens.controller_tab import controller_tab
from src.admin.screens.task_controller import employer_tab

class AdminPanel(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            scrollable=True,
            tabs=[
                ft.Tab(text="Главная", content=home_tab(page)),
                ft.Tab(text="Поиск", content=search_tab(page)),
                ft.Tab(text="Назначение", content=assignment_tab(page)),
                ft.Tab(text="Контроллеры", content=controller_tab(page)),
            ],
            expand=1,
        )

    def build(self):
        return self.tabs

    def add_new_tab(self, selected_rows):
        new_tab = ft.Tab(text="Назначение - Задач", content=employer_tab(self.page, selected_rows))
        self.tabs.tabs.append(new_tab)
        self.tabs.selected_index = len(self.tabs.tabs) - 1
        self.tabs.update()

    def return_tab(self):
        if len(self.tabs.tabs) > 1:
            self.tabs.tabs.pop()
            self.tabs.selected_index = len(self.tabs.tabs) - 2
            self.tabs.update()
        else:
            print("Нельзя удалить последнюю вкладку")

def admin_main(page):
    page.title = "Admin Panel"
    page.controls.clear()
    admin_panel = AdminPanel(page)
    page.add(admin_panel)
    page.update()

    # Обновите глобальные функции, чтобы они использовали методы AdminPanel
    global add_new_tab, return_tab
    add_new_tab = admin_panel.add_new_tab
    return_tab = admin_panel.return_tab