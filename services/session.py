from dto.user import UserRole


class SessionService:
    def __init__(self):
        self.current_user = None

    def set_user(self, user):
        self.current_user = user

    def clear(self):
        self.current_user = None

    def is_admin(self):
        if not self.current_user:
            return False

        return self.current_user.type == UserRole.ADMIN.value

    def is_authorized(self):
        return self.current_user != None
