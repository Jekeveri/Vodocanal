import flet as ft

class CommonTable(ft.UserControl):
    def __init__(self, columns, get_data_func, on_row_select, on_action):
        super().__init__()
        self.columns = columns
        self.get_data_func = get_data_func
        self.on_row_select = on_row_select
        self.on_action = on_action
        self.selected_rows = set()
        self.search_input = ft.TextField(label="Поиск", width=300, on_change=self.update_table)
        self.filter_dropdown = ft.Dropdown(
            label="Фильтр",
            options=[
                ft.dropdown.Option("Все"),
                ft.dropdown.Option("По адресу"),
                ft.dropdown.Option("По ФИО"),
            ],
            value="Все",
            on_change=self.update_table
        )
        self.data_table = ft.DataTable(
            columns=self.columns,
            rows=[],
            border=ft.border.all(2, "grey"),
            border_radius=10,
            data_row_max_height=100,
            vertical_lines=ft.BorderSide(1, "grey"),
            horizontal_lines=ft.BorderSide(1, "grey"),
        )

    def build(self):
        return ft.Column([
            ft.Row([self.search_input, self.filter_dropdown]),
            ft.Container(
                content=self.data_table,
                height=400,
                expand=True,
                scroll=ft.ScrollMode.AUTO
            ),
            ft.Row([
                ft.ElevatedButton("Действие", on_click=self.on_action)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])

    def update_table(self, e=None):
        search_value = self.search_input.value.lower()
        filter_value = self.filter_dropdown.value

        try:
            results = self.get_data_func()
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return

        filtered_results = self.filter_results(results, search_value, filter_value)

        self.data_table.rows.clear()
        for row_data in filtered_results:
            self.data_table.rows.append(self.create_row(row_data))
        self.update()

    def filter_results(self, results, search_value, filter_value):
        # Реализуйте фильтрацию в соответствии с вашими требованиями
        return results

    def create_row(self, row_data):
        # Реализуйте создание строки таблицы в соответствии с вашими данными
        pass

    def select_row(self, row_id, is_selected):
        if is_selected:
            self.selected_rows.add(row_id)
        else:
            self.selected_rows.discard(row_id)
        self.on_row_select(self.selected_rows)
        self.update_table()