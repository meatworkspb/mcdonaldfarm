from argon2 import PasswordHasher


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def authorize(self, username: str, password: str):
        user = self.user_repository.find_by_username(username)
        if not user:
            return False

        ph = PasswordHasher()
        try:
            ph.verify(user.password, password)
        except Exception:
            return False

        return user
