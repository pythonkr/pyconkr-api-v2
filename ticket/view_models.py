from dataclasses import asdict, dataclass
from typing import Optional

from .models import ConferenceTicketType


@dataclass(init=False)
class ConferenceTicketTypeViewModel:
    code: str
    name: str
    price: int
    min_price: Optional[int]
    desc: str
    day: str

    def __init__(self, model: ConferenceTicketType):
        self.code = model.code
        self.name = model.name
        self.price = model.price
        self.min_price = model.min_price
        self.desc = model.desc
        self.day = model.day

    def to_dict(self):
        return asdict(self)
