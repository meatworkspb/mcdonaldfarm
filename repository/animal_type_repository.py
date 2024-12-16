from dto.animal_type import AnimalType


class AnimalTypeRepository:
    def __init__(self, database) -> None:
        self.db = database

    def find_by_id(self, id: int):
        sql = "select * from animal_type where id = %s"
        animal_type = self.db.get_one(sql, (id,))

        if not animal_type:
            return None

        return AnimalType(**dict(animal_type))

    def find_all(self):
        sql = "select * from animal_type"
        animal_types = self.db.get_all(sql)
        if not animal_types:
            return None

        objects = []
        for type_ in animal_types:
            objects.append(AnimalType(**dict(type_)))

        return objects

    def create(self, name: str):
        sql = "insert into animal_type (name) values (%s)"
        self.db.execute_query(sql, (name,))

    def update(self, id: int, name: str):
        sql = "update animal_type set name = %s where id = %s"
        self.db.execute_query(sql, (name, id))

    def delete(self, id: int):
        sql = "delete from animal_type where id = %s"
        self.db.execute_query(sql, (id,))
