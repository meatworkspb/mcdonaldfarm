import tkinter as tk


class MenuView(tk.Frame):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.create_menu()

    def create_menu(self):
        self.menu_frame = tk.Frame(self.app.root)
        self.menu_frame.pack(side="top", fill="x")

        self.animal_btn = tk.Button(
            self.menu_frame,
            text="Животные",
            command=lambda: self.app.handle_route("animal"),
        )
        self.animal_type_btn = tk.Button(
            self.menu_frame,
            text="Типы животных",
            command=lambda: self.app.handle_route("animal_type"),
        )
        self.logout_btn = tk.Button(
            self.menu_frame,
            text="Выход",
            command=lambda: self.app.handle_route("logout"),
        )

        self.animal_btn.pack(side="left", padx=5, pady=5)
        self.animal_type_btn.pack(side="left", padx=5, pady=5)
        self.logout_btn.pack(side="left", padx=5, pady=5)
        self.menu_frame.pack_forget()

    def hide_menu(self):
        self.menu_frame.pack_forget()

    def show_menu(self):
        self.menu_frame.pack(side="top", fill="x")
