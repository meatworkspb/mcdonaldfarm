from dto.user import UserRole
from repository.user_repository import UserRepository
from services.database import Database


if __name__ == "__main__":
    db = Database(
        {"dsn": "dbname=farm user=farm password=farm host=127.0.0.1 port=5432"}
    )

    with open("./database.sql", "r") as f:
        sql_data = f.read()
        db.execute_script(sql_data)

    user_repo = UserRepository(db)
    user_repo.create_user("admin", "admin", UserRole.ADMIN)
    user_repo.create_user("user", "user", UserRole.USER)
