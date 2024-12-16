from dataclasses import dataclass
from datetime import date


@dataclass
class Animal:
    id: int
    name: str
    type_id: int
    weight: float
    dob: date
    sex: str
