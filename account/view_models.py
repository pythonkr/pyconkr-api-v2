from dataclasses import dataclass, asdict

from ticket.models import Ticket


@dataclass(init=False)
class UserTicketInfo:
    ticket_type_name: str
    date: str
    price: int
    payment_key: str

    def __init__(self, ticket: Ticket):
        self.ticket_type_name = ticket.ticket_type.name
        self.date = ticket.ticket_type.day
        self.price = ticket.payment.money
        self.payment_key = ticket.payment.payment_key

    def to_dict(self):
        return asdict(self)
