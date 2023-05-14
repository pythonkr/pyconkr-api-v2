from django.contrib.auth import get_user_model
from django.db import transaction

from payment.models import Payment
from ticket.models import TicketType

import shortuuid

User = get_user_model()


@transaction.atomic
def generate_payment_key(user: User, ticket_type: TicketType):
    new_payment = Payment(
        payment_key=shortuuid.uuid(),
        user_id=user,
        # ticket_type=ticket_type,      # TODO
        money=ticket_type.price
    )

    new_payment.save()

    return new_payment.payment_key
