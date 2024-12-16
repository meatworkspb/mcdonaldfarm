from argon2 import PasswordHasher

from dto.user import User, UserRole


class UserRepository:
    def __init__(self, database) -> None:
        self.db = database

    def find_by_username(self, username: str):
        sql = "SELECT * FROM users WHERE username = %s"
        user = self.db.get_one(sql, (username,))
        if user:
            return User(**dict(user))
        else:
            return None

    def create_user(self, username, password, type=UserRole.USER):
        ph = PasswordHasher()
        sql = "INSERT INTO users (username, password, type) VALUES (%s, %s, %s)"
        self.db.execute_query(sql, (username, ph.hash(password), type.value))
