from views.animal_type_form import AnimalTypeForm


class AnimalTypeController:
    def __init__(self, app):
        self.app = app
        self.view = AnimalTypeForm(self)

    def clear(self):
        self.view.destroy()

    def load_data(self):
        types = self.app.repositories["animal_types"].find_all()
        return types

    def handle_create(self, name):
        try:
            self.app.repositories["animal_types"].create(name)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False

        return True

    def handle_update(self, id: int, name: str):
        try:
            self.app.repositories["animal_types"].update(id, name)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False

        return True

    def handle_delete(self, id: int):
        try:
            self.app.repositories["animal_types"].delete(id)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False

        return True
