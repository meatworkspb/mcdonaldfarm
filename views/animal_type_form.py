import tkinter as tk
from tkinter import ttk


class AnimalTypeForm(tk.Frame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        tk.Label(self, text="Типы животынх", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(
            self, columns=("ID", "Name"), show="headings", height=15
        )
        self.tree.pack(pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        if self.controller.app.services["session"].is_admin():
            # Кнопки
            button_frame = tk.Frame(self)
            button_frame.pack(pady=10)

            tk.Button(button_frame, text="Создать", command=self.add_animal_type).grid(
                row=0, column=0, padx=5
            )
            tk.Button(
                button_frame, text="Редактировать", command=self.edit_animal_type
            ).grid(row=0, column=1, padx=5)
            tk.Button(
                button_frame, text="Удалить", command=self.delete_animal_type
            ).grid(row=0, column=2, padx=5)

            self.result_label = tk.Label(self, text="", fg="red")
            self.result_label.pack(pady=10)

    def result_message(self, message: str):
        self.result_label.config(text=message)

    def load_data(self):
        animal_types = self.controller.load_data()
        if not animal_types:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in animal_types:
            self.tree.insert("", "end", values=(item.id, item.name))

    def on_select_item(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

    def add_animal_type(self):
        name = self.name_entry.get().strip()

        if name == "":
            return

        result = self.controller.handle_create(name)
        if result:
            self.result_message("Тип успешно создан!")
            self.load_data()
        else:
            self.result_message("Ошибка создания типа!")

    def edit_animal_type(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.result_message("Выберите тип для редактирования!")
            return

        name = self.name_entry.get().strip()
        if not name:
            self.result_message("Имя не указано!")
            return

        values = self.tree.item(selected_item[0], "values")
        item_id = values[0]

        result = self.controller.handle_update(item_id, name)
        if result:
            self.result_message("Тип успешно обновлен!")
            self.load_data()
        else:
            self.result_message("Ошибка обновления типа!")

    def delete_animal_type(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.result_message("Выберите тип для удаления")
            return

        values = self.tree.item(selected_item[0], "values")
        item_id = values[0]

        result = self.controller.handle_delete(item_id)
        if result:
            self.result_message("Тип успешно удален!")
            self.load_data()
        else:
            self.result_message("Ошибка удаления типа!")
