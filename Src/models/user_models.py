from typing import Dict
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str


items: Dict[int, Item] = {}
