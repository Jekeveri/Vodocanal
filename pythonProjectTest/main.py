import flet as ft
from datetime import datetime, timedelta
import warnings

# Suppress the specific DeprecationWarning for UserControl
warnings.filterwarnings("ignore", category=DeprecationWarning, message="UserControl is deprecated")

class TaskStatus:
    NOT_STARTED = "Не начато"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Выполнено"
    OVERDUE = "Просрочено"

class Task:
    def __init__(self, title, description, category, priority, due_date, status=TaskStatus.NOT_STARTED):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.status = status


def get_status_icon_and_color(task):
    if task.status == TaskStatus.COMPLETED:
        return ft.icons.CHECK_CIRCLE, ft.colors.GREEN
    elif task.status == TaskStatus.OVERDUE or (task.status != TaskStatus.COMPLETED and task.due_date < datetime.now()):
        return ft.icons.ERROR, ft.colors.RED
    elif task.status == TaskStatus.IN_PROGRESS:
        return ft.icons.PENDING, ft.colors.ORANGE
    else:
        return ft.icons.SCHEDULE, ft.colors.GREY


class TaskList(ft.UserControl):
    def __init__(self, tasks, on_task_click):
        super().__init__()
        self.task_list = None
        self.tasks = tasks
        self.on_task_click = on_task_click

    def build(self):
        self.task_list = ft.ListView(expand=1, spacing=10, padding=20)
        self.update_task_list()
        return self.task_list

    def update_task_list(self, search_term="", category="Все", sort_by_priority=False):
        self.task_list.controls.clear()
        filtered_tasks = self.tasks
        if sort_by_priority:
            filtered_tasks.sort(key=lambda x: x.priority, reverse=True)
        for task in filtered_tasks:
            if (search_term.lower() in task.title.lower() or search_term.lower() in task.description.lower()) and \
               (category == "Все" or category == task.category):
                self.task_list.controls.append(self.create_task_item(task))
        self.update()

    def create_task_item(self, task):
        status_icon, status_color = get_status_icon_and_color(task)
        return ft.ListTile(
            leading=ft.Icon(status_icon, color=status_color),
            title=ft.Text(task.title, style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
            subtitle=ft.Text(f"{task.description} | Приоритет: {task.priority} | Срок: {task.due_date.strftime('%d.%m.%Y')}"),
            trailing=ft.Text(task.category),
            on_click=lambda _: self.on_task_click(task),
        )


class TaskDetails(ft.UserControl):
    def __init__(self, task, on_save, on_delete):
        super().__init__()
        self.status_dropdown = None
        self.due_date_button = None
        self.due_date_picker = None
        self.priority_slider = None
        self.category_dropdown = None
        self.description_field = None
        self.title_field = None
        self.task = task
        self.on_save = on_save
        self.on_delete = on_delete

    def build(self):
        self.title_field = ft.TextField(label="Название", value=self.task.title)
        self.description_field = ft.TextField(label="Описание", value=self.task.description)
        self.category_dropdown = ft.Dropdown(
            label="Категория",
            options=[
                ft.dropdown.Option("Личное"),
                ft.dropdown.Option("Работа"),
                ft.dropdown.Option("Здоровье"),
                ft.dropdown.Option("Дом"),
            ],
            value=self.task.category,
        )
        self.priority_slider = ft.Slider(min=1, max=5, divisions=4, label="Приоритет", value=self.task.priority)
        self.due_date_picker = ft.DatePicker(
            on_change=self.change_date,
            first_date=datetime(2023, 1, 1),
            last_date=datetime(2030, 12, 31),
        )
        self.due_date_button = ft.ElevatedButton(
            "Выбрать срок",
            icon=ft.icons.CALENDAR_TODAY,
            on_click=lambda _: self.due_date_picker.pick_date(),
        )
        self.status_dropdown = ft.Dropdown(
            label="Статус",
            options=[
                ft.dropdown.Option(TaskStatus.NOT_STARTED),
                ft.dropdown.Option(TaskStatus.IN_PROGRESS),
                ft.dropdown.Option(TaskStatus.COMPLETED),
                ft.dropdown.Option(TaskStatus.OVERDUE),
            ],
            value=self.task.status,
        )

        return ft.Column([
            self.title_field,
            self.description_field,
            self.category_dropdown,
            self.priority_slider,
            ft.Row([self.due_date_button, ft.Text(self.task.due_date.strftime("%d.%m.%Y"))]),
            self.status_dropdown,
            ft.Row([
                ft.ElevatedButton("Сохранить", on_click=self.save_task),
                ft.ElevatedButton("Удалить", on_click=self.delete_task, color=ft.colors.RED_400),
            ]),
        ])

    def change_date(self, e):
        self.task.due_date = e.date
        self.due_date_button.text = f"Срок: {e.date.strftime('%d.%m.%Y')}"
        self.update()

    def save_task(self, e):
        self.task.title = self.title_field.value
        self.task.description = self.description_field.value
        self.task.category = self.category_dropdown.value
        self.task.priority = int(self.priority_slider.value)
        self.task.status = self.status_dropdown.value
        self.on_save(self.task)

    def delete_task(self, e):
        self.on_delete(self.task)


class TaskManager(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.sort_switch = None
        self.search_field = None
        self.category_dropdown = None
        self.page = page
        self.tasks = [
            Task("Покупки", "Купить продукты", "Личное", 3, datetime.now() + timedelta(days=1)),
            Task("Отчет", "Подготовить квартальный отчет", "Работа", 5, datetime.now() + timedelta(days=3), TaskStatus.IN_PROGRESS),
            Task("Тренировка", "Сходить в спортзал", "Здоровье", 2, datetime.now() - timedelta(days=1), TaskStatus.OVERDUE),
            Task("Уборка", "Убрать квартиру", "Дом", 1, datetime.now() - timedelta(days=2), TaskStatus.COMPLETED),
        ]
        self.task_list = TaskList(self.tasks, self.show_task_details)

    def build(self):
        self.search_field = ft.TextField(label="Поиск", expand=True)
        self.category_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("Все"),
                ft.dropdown.Option("Личное"),
                ft.dropdown.Option("Работа"),
                ft.dropdown.Option("Здоровье"),
                ft.dropdown.Option("Дом"),
            ],
            value="Все",
            expand=True,
        )
        self.sort_switch = ft.Switch(label="Сортировать по приоритету", value=False)

        return ft.Column([
            ft.Row([self.search_field, self.category_dropdown]),
            ft.Row([
                ft.ElevatedButton("Поиск", on_click=self.search_tasks),
                self.sort_switch,
            ]),
            self.task_list,
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_task),
        ])

    def search_tasks(self, e):
        self.task_list.update_task_list(self.search_field.value, self.category_dropdown.value, self.sort_switch.value)

    def show_task_details(self, task):
        self.page.go(f"/task/{self.tasks.index(task)}")

    def add_task(self, e):
        new_task = Task("Новое задание", "", "Личное", 3, datetime.now() + timedelta(days=7))
        self.tasks.append(new_task)
        self.show_task_details(new_task)


class SettingsView(ft.UserControl):
    def build(self):
        return ft.Column([
            ft.Text("Настройки", size=20, weight=ft.FontWeight.BOLD),
            ft.Switch(label="Темный режим", value=self.page.theme_mode == ft.ThemeMode.DARK, on_change=self.toggle_theme),
        ])

    def toggle_theme(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        self.page.update()


def main(page: ft.Page):
    page.title = "Менеджер задач с статусами"
    page.theme_mode = ft.ThemeMode.DARK

    # Add some initial content to test
    page.add(ft.Text("Welcome to the Task Manager!", size=30))

    task_manager = TaskManager(page)
    settings_view = SettingsView()

    def route_change(route):
        page.views.clear()
        print(f"Current route: {page.route}")  # Debugging
        if page.route == "/":
            print("Loading main task view...")
            page.views.append(
                ft.View(
                    "/",
                    [
                        task_manager,
                        ft.NavigationBar(
                            destinations=[
                                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Задания"),
                                ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Настройки"),
                            ],
                            on_change=lambda e: page.go("/settings" if e.control.selected_index == 1 else "/"),
                        ),
                    ],
                )
            )
        elif page.route == "/settings":
            print("Loading settings view...")
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        settings_view,
                        ft.NavigationBar(
                            destinations=[
                                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Задания"),
                                ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Настройки"),
                            ],
                            selected_index=1,
                            on_change=lambda e: page.go("/settings" if e.control.selected_index == 1 else "/"),
                        ),
                    ],
                )
            )
        elif page.route.startswith("/task/"):
            task_id = int(page.route.split("/")[-1])
            task = task_manager.tasks[task_id]
            print(f"Loading task {task_id} details...")
            page.views.append(
                ft.View(
                    f"/task/{task_id}",
                    [
                        TaskDetails(task, on_save=lambda _: page.go("/"), on_delete=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    page.update()

ft.app(target=main)
