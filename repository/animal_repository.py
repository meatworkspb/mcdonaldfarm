from dto.animal import Animal


class AnimalRepository:
    def __init__(self, database) -> None:
        self.db = database

    def find_by_id(self, id: int):
        sql = "SELECT * FROM animal WHERE id = %s"
        animal = self.db.get_one(sql, (id,))
        if not animal:
            return None
        return Animal(**dict(animal))

    def find_all(self):
        sql = "SELECT * FROM animal"
        animals = self.db.get_all(sql)
        if not animals:
            return None

        return [Animal(**dict(animal)) for animal in animals]

    def create(self, name: str, type_id: int, weight: float, dob: str, sex: str):
        sql = "INSERT INTO animal (name, type_id, weight, dob, sex) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute_query(sql, (name, type_id, weight, dob, sex))

    def update(
        self, id: int, name: str, type_id: int, weight: float, dob: str, sex: str
    ):
        sql = """
        UPDATE animal 
        SET name = %s, type_id = %s, weight = %s, dob = %s, sex = %s 
        WHERE id = %s
        """
        self.db.execute_query(sql, (name, type_id, weight, dob, sex, id))

    def delete(self, id: int):
        sql = "DELETE FROM animal WHERE id = %s"
        self.db.execute_query(sql, (id,))

    def find_by_filters(self, filters):
        sql = "SELECT * FROM animal WHERE 1=1"
        params = []

        if filters.get("name"):
            sql += " AND LOWER(name) LIKE LOWER(%s)"
            params.append(f"%{filters['name']}%")

        if filters.get("type_id"):
            sql += " AND type_id = %s"
            params.append(filters["type_id"])

        if filters.get("weight_min"):
            sql += " AND weight >= %s"
            params.append(filters["weight_min"])

        if filters.get("weight_max"):
            sql += " AND weight <= %s"
            params.append(filters["weight_max"])

        if filters.get("dob_from"):
            sql += " AND dob >= %s"
            params.append(filters["dob_from"])

        if filters.get("dob_to"):
            sql += " AND dob <= %s"
            params.append(filters["dob_to"])

        if filters.get("sex_male") and not filters.get("sex_female"):
            sql += " AND sex = %s"
            params.append("M")
        elif filters.get("sex_female") and not filters.get("sex_male"):
            sql += " AND sex = %s"
            params.append("F")

        result = self.db.get_all(sql, params)
        return [Animal(**dict(row)) for row in result] if result else []
