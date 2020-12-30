from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Advertisement:
    id: Optional[int]
    ref: str
    name: str
    description: str
    price : int
    source: str
    url: str
    house_area: int
    garden_area: int
    picture_url: str
    localization: str
    date: datetime
    type: str