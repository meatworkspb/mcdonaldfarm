from views.login_form import LoginFormView


class AuthController:
    def __init__(self, app):
        self.app = app
        self.view = LoginFormView(self)

    def clear(self):
        self.view.destroy()

    def handle_login(self, username: str, password: str):
        user = self.app.services["auth"].authorize(username, password)
        if not user:
            self.view.show_error("Ошибка авторизации")
            return

        self.app.services["session"].set_user(user)
        self.app.handle_route("animal")
