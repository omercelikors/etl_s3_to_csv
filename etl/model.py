from dataclasses import dataclass
from datetime import date

@dataclass
class RateModel:
    date: date
    code: str
    unit: int
    name: str
    buying: float
    selling: float


