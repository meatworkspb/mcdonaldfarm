import tkinter as tk


class LoginFormView(tk.Frame):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Авторизация", font=("Arial", 18, "bold")).pack(
            pady=(10, 20)
        )

        tk.Label(self, text="Имя пользователя:", font=("Arial", 12)).pack(
            anchor="w", pady=(5, 2)
        )
        self.username_field = tk.Entry(self, font=("Arial", 12))
        self.username_field.pack(fill="x", pady=(0, 10))

        tk.Label(self, text="Пароль:", font=("Arial", 12)).pack(anchor="w", pady=(5, 2))
        self.password_field = tk.Entry(self, show="*", font=("Arial", 12))
        self.password_field.pack(fill="x", pady=(0, 20))

        tk.Button(
            self,
            text="Вход",
            command=self.login_click,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            relief="raised",
        ).pack(pady=(0, 10))

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial", 10))
        self.error_label.pack()

    def login_click(self):
        self.controller.handle_login(
            self.username_field.get(), self.password_field.get()
        )

    def show_error(self, message: str):
        self.error_label.config(text=message)
