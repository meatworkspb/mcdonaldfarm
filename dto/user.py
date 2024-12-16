from dataclasses import dataclass
from enum import Enum


class UserRole(Enum):
    USER = 0
    ADMIN = 1


@dataclass
class User:
    id: int
    username: str
    password: str
    type: UserRole
