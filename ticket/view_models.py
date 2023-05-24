from dataclasses import asdict, dataclass
from typing import Optional

from .models import TicketType


@dataclass(init=False)
class TicketTypeViewModel:
    id: str
    name: str
    price: int
    min_price: Optional[int]
    desc: str
    day: str  # choice
    # program: ...
    is_refundable: bool

    def __init__(self, model: TicketType):
        self.id = model.id
        self.name = model.name
        self.price = model.price
        self.min_price = model.min_price
        self.desc = model.desc
        self.day = model.day
        self.is_refundable = model.is_refundable

    def to_dict(self):
        return asdict(self)
