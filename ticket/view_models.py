from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional, Union

from program.models import CONFERENCE, TUTORIAL, SPRINT
from .models import TicketType


@dataclass(init=False)
class TicketTypeViewModel:
    @dataclass
    class Program:
        title: str
        short_desc: str
        start_at: datetime
        end_at: datetime
        program_type: str  # type: Union[CONFERENCE, TUTORIAL, SPRINT]

    id: str
    name: str
    price: int
    min_price: Optional[int]
    desc: str
    day: str  # choice
    program: Program
    is_refundable: bool
    is_buyable: property  # type: bool

    def __init__(self, model: TicketType):
        self.id = str(model.id)
        self.name = model.name
        self.price = model.price
        self.min_price = model.min_price
        self.desc = model.desc
        self.day = model.day
        self.program = TicketTypeViewModel.Program(
            title=model.program.title,
            short_desc=model.program.short_desc,
            start_at=model.program.start_at,
            end_at=model.program.end_at,
            program_type=model.program.program_type,
        )
        self.is_refundable = model.is_refundable
        self.is_buyable = model.buyable

    def to_dict(self):
        return asdict(self)
