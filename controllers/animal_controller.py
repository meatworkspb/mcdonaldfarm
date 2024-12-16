from views.animal_form import AnimalForm


class AnimalController:
    def __init__(self, app):
        self.app = app
        self.view = AnimalForm(self)

    def clear(self):
        self.view.destroy()

    def load_animal_types(self):
        animal_types = self.app.repositories["animal_types"].find_all()
        return animal_types

    def load_data(self):
        animals = self.app.repositories["animals"].find_all()
        return animals

    def handle_create(self, name, type_id, weight, dob, sex):
        try:
            self.app.repositories["animals"].create(name, type_id, weight, dob, sex)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False
        return True

    def handle_update(self, id, name, type_id, weight, dob, sex):
        try:
            self.app.repositories["animals"].update(id, name, type_id, weight, dob, sex)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False
        return True

    def handle_delete(self, id: int):
        try:
            self.app.repositories["animals"].delete(id)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return False
        return True

    def filter_animals(self, filters):
        try:
            return self.app.repositories["animals"].find_by_filters(filters)
        except Exception as ex:
            if self.app.mode == "debug":
                print(ex)
            return []
