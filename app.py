import tkinter as tk
from services.auth_service import AuthService
from services.database import Database
from services.session import SessionService
from controllers.animal_controller import AnimalController
from controllers.animal_type import AnimalTypeController
from controllers.auth import AuthController
from repository.animal_repository import AnimalRepository
from repository.animal_type_repository import AnimalTypeRepository
from repository.user_repository import UserRepository
from views.menu import MenuView


class App:
    def __init__(self):
        self.services = {}
        self.repositories = {}

        self.mode = "prod"

        self.services["database"] = Database(
            {"dsn": "dbname=farm user=farm password=farm host=127.0.0.1 port=5432"}
        )
        self.repositories = {
            "users": UserRepository(self.services["database"]),
            "animal_types": AnimalTypeRepository(self.services["database"]),
            "animals": AnimalRepository(self.services["database"]),
        }

        self.services["auth"] = AuthService(self.repositories["users"])
        self.services["session"] = SessionService()

        self.root = tk.Tk()
        self.root.title("Ферма старого МакДоналда")
        self.root.geometry("700x900")
        self.menu_view = MenuView(self)

        self.current_controller = None

    def switch_controller(self, controller):
        if self.current_controller:
            self.current_controller.clear()

        self.current_controller = controller(self)

    def handle_route(self, route):
        if route == "logout":
            self.services["session"].clear()
            self.menu_view.hide_menu()

        if self.services["session"].is_authorized():
            self.menu_view.show_menu()

        if route == "login":
            self.switch_controller(AuthController)
        elif route == "logout":
            self.switch_controller(AuthController)
        elif route == "animal_type":
            self.switch_controller(AnimalTypeController)
        elif route == "animal":
            self.switch_controller(AnimalController)

    def run(self):
        self.handle_route("login")
        self.root.mainloop()
