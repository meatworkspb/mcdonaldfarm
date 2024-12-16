import tkinter as tk
from tkinter import ttk, messagebox


class AnimalForm(tk.Frame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        tk.Label(self, text="Животные", font=("Arial", 16)).pack(pady=10)

        self._create_simple_filter()
        self._create_advanced_filter()
        self._create_table()
        self._create_edit_form()

    def _create_simple_filter(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтровать по имени:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.filter_entry = tk.Entry(filter_frame, width=30)
        self.filter_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(
            filter_frame, text="Фильтровать", command=self.filter_animals_simple
        ).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.load_data).grid(
            row=0, column=3, padx=5
        )

    def _create_edit_form(self):
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
        self.type_combobox = ttk.Combobox(form_frame, state="readonly", width=18)
        self.type_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Вес:").grid(row=2, column=0, padx=5, pady=5)
        self.weight_entry = tk.Entry(form_frame, width=20)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Дата рождения:").grid(
            row=3, column=0, padx=5, pady=5
        )
        self.dob_entry = tk.Entry(form_frame, width=20)
        self.dob_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(
            form_frame,
            text="Формат: YYYY-MM-DD",
            font=("Arial", 8, "italic"),
            fg="gray",
        ).grid(row=4, column=1, sticky="w")

        tk.Label(form_frame, text="Пол:").grid(row=5, column=0, padx=5, pady=5)
        self.sex_var = tk.StringVar(value="M")
        male_radio = tk.Radiobutton(
            form_frame, text="М", variable=self.sex_var, value="M"
        )
        female_radio = tk.Radiobutton(
            form_frame, text="Ж", variable=self.sex_var, value="F"
        )
        male_radio.grid(row=5, column=1, sticky="w")
        female_radio.grid(row=5, column=1, sticky="e")

        if self.controller.app.services["session"].is_admin():
            button_frame = tk.Frame(self)
            button_frame.pack(pady=10)

            tk.Button(button_frame, text="Создать", command=self.add_animal).grid(
                row=0, column=0, padx=5
            )
            tk.Button(
                button_frame, text="Редактировать", command=self.edit_animal
            ).grid(row=0, column=1, padx=5)
            tk.Button(button_frame, text="Удалить", command=self.delete_animal).grid(
                row=0, column=2, padx=5
            )

            self.result_label = tk.Label(self, text="", fg="red")
            self.result_label.pack(pady=10)

    def _create_table(self):
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Name", "Type", "Weight", "DOB", "Sex"),
            show="headings",
            height=15,
        )
        self.tree.pack(pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Weight", text="Вес")
        self.tree.heading("DOB", text="Дата рождения")
        self.tree.heading("Sex", text="Пол")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Weight", width=100, anchor="center")
        self.tree.column("DOB", width=100, anchor="center")
        self.tree.column("Sex", width=50, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    def _create_advanced_filter(self):
        self.advanced_filter_visible = False

        self.advanced_filter_button_frame = tk.Frame(self)
        self.advanced_filter_button_frame.pack(pady=10)

        self.advanced_filter_frame = tk.Frame(self)

        self.toggle_button = tk.Button(
            self.advanced_filter_button_frame,
            text="Расширенный фильтр",
            command=self.toggle_advanced_filter,
        )
        self.toggle_button.grid(row=0, column=0, columnspan=3, pady=5)

        tk.Label(self.advanced_filter_frame, text="Имя:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_name_entry = tk.Entry(self.advanced_filter_frame, width=20)
        self.fil_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Тип:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_type_combobox = ttk.Combobox(
            self.advanced_filter_frame, state="readonly", width=18
        )
        self.fil_type_combobox.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Вес >").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_weight_min_entry = tk.Entry(self.advanced_filter_frame, width=20)
        self.fil_weight_min_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Вес <").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_weight_max_entry = tk.Entry(self.advanced_filter_frame, width=20)
        self.fil_weight_max_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Дата рождения >").grid(
            row=4, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_dob_from_entry = tk.Entry(self.advanced_filter_frame, width=20)
        self.fil_dob_from_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Дата рождения <").grid(
            row=5, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_dob_to_entry = tk.Entry(self.advanced_filter_frame, width=20)
        self.fil_dob_to_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.advanced_filter_frame, text="Пол:").grid(
            row=6, column=0, padx=5, pady=5, sticky="e"
        )
        self.fil_sex_male_var = tk.BooleanVar(value=False)
        self.fil_sex_female_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.advanced_filter_frame, text="М", variable=self.fil_sex_male_var
        ).grid(row=6, column=1, sticky="w")
        tk.Checkbutton(
            self.advanced_filter_frame, text="Ж", variable=self.fil_sex_female_var
        ).grid(row=6, column=1, sticky="e")

        button_frame = tk.Frame(self.advanced_filter_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(
            button_frame,
            text="Применить фильтр",
            command=self.apply_advanced_filter,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Сброс",
            command=self.load_data,
        ).grid(row=0, column=1, padx=5)

        self.advanced_filter_frame.pack_forget()

    def toggle_advanced_filter(self):
        if self.advanced_filter_visible:
            self.advanced_filter_frame.pack_forget()
            self.toggle_button.config(text="Расширенный фильтр")
        else:
            self.advanced_filter_frame.pack(
                pady=10,
                # fill="x",
                after=self.advanced_filter_button_frame,
                anchor="center",
            )
            self.toggle_button.config(text="Скрыть расширенный фильтр")
        self.advanced_filter_visible = not self.advanced_filter_visible

    def apply_advanced_filter(self):
        filters = {
            "name": self.fil_name_entry.get().strip(),
            "weight_min": self.fil_weight_min_entry.get().strip(),
            "weight_max": self.fil_weight_max_entry.get().strip(),
            "dob_from": self.fil_dob_from_entry.get().strip(),
            "dob_to": self.fil_dob_to_entry.get().strip(),
            "sex_male": self.fil_sex_male_var.get(),
            "sex_female": self.fil_sex_female_var.get(),
        }
        if self.fil_type_combobox.get() and self.fil_type_combobox.get() != "--":
            filters["type_id"] = self.animal_type_value_to_id[
                self.fil_type_combobox.get()
            ]

        self.load_data(filters)

    def filter_animals_simple(self):
        filters = {"name": self.filter_entry.get().strip()}
        self.load_data(filters)

    def _populate_table(self, animals):
        if not animals and animals != []:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in animals:
            try:
                type_value = self.animal_type_id_to_value[item.type_id]
            except:
                type_value = "ошибка"
            self.tree.insert(
                "",
                "end",
                values=(
                    item.id,
                    item.name,
                    type_value,
                    item.weight,
                    item.dob,
                    item.sex,
                ),
            )

    def result_message(self, message: str):
        self.result_label.config(text=message)

    def load_data(self, filters=None):
        self.animal_types = self.controller.load_animal_types()

        if self.animal_types:
            self.animal_type_id_to_value = {
                atype.id: atype.name for atype in self.animal_types
            }
            self.animal_type_value_to_id = {
                atype.name: atype.id for atype in self.animal_types
            }
        else:
            self.animal_type_id_to_value = {}
            self.animal_type_value_to_id = {}

        if self.animal_types:
            self.type_combobox["values"] = [
                f"{type_.name}" for type_ in self.animal_types
            ]
            self.fil_type_combobox["values"] = [
                f"{type_.name}" for type_ in self.animal_types
            ]
            self.fil_type_combobox["values"] = ("--",) + self.fil_type_combobox[
                "values"
            ]

        if filters:
            animals = self.controller.filter_animals(filters)
        else:
            animals = self.controller.load_data()

        self._populate_table(animals)

    def on_select_item(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.type_combobox.set(f"{values[2]}")
        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(0, values[3])
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, values[4])
        self.sex_var.set(values[5])

    def add_animal(self):
        name = self.name_entry.get().strip()
        try:
            type_id = self.animal_type_value_to_id[self.type_combobox.get()]
        except:
            self.result_message("Ошибка создания животного!")

        weight = self.weight_entry.get().strip()
        dob = self.dob_entry.get().strip()
        sex = self.sex_var.get()

        if not name or not type_id or not weight or not dob or not sex:
            self.result_message("Все поля обязательны к заполнению!")
            return

        result = self.controller.handle_create(name, type_id, float(weight), dob, sex)
        if result:
            self.result_message("Животное успешно создано!")
            self.load_data()
        else:
            self.result_message("Ошибка создания животного")

    def edit_animal(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.result_message("Выберите животное для редактирования!")
            return

        values = self.tree.item(selected_item[0], "values")
        item_id = values[0]

        name = self.name_entry.get().strip()
        type_id = self.animal_type_value_to_id[self.type_combobox.get()]
        weight = self.weight_entry.get().strip()
        dob = self.dob_entry.get().strip()
        sex = self.sex_var.get()

        if not name or not type_id or not weight or not dob or not sex:
            self.result_message("Все поля обязательны к заполнению!")
            return

        result = self.controller.handle_update(
            item_id, name, type_id, float(weight), dob, sex
        )
        if result:
            self.result_message("Животное успешно обновлено!")
            self.load_data()
        else:
            self.result_message("Ошибка обновления животного!")

    def delete_animal(self):
        selected_item = self.tree.selection()
        if not selected_item:
            self.result_message("Выберите животное для удаления!")
            return

        values = self.tree.item(selected_item[0], "values")
        item_id = values[0]

        confirm = messagebox.askyesno(
            "Подтвердите удаление",
            f"Подтвердите удаление '{values[1]}'",
        )
        if confirm:
            result = self.controller.handle_delete(item_id)
            if result:
                self.result_message("Животное успешно удалено!")
                self.load_data()
            else:
                self.result_message("Ошибка удаления животного!")
