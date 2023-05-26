from django.contrib.auth import get_user_model
from django.db import transaction

from payment.enum import PaymentStatus
from payment.models import Payment, PaymentHistory
from ticket.models import TicketType, Ticket

import shortuuid

User = get_user_model()


@transaction.atomic
def generate_payment_key(user: User, ticket_type: TicketType):
    new_payment = Payment(
        payment_key=shortuuid.uuid(),
        user=user,
        ticket_type=ticket_type,
        money=ticket_type.price,
        status=PaymentStatus.BEFORE_PAYMENT.value
    )

    new_payment.save()

    _save_history(new_payment.payment_key, PaymentStatus.BEFORE_PAYMENT.value)
    return new_payment.payment_key


@transaction.atomic
def proceed_payment(payment_key: str, is_succeed: bool):
    status_value = PaymentStatus.PAYMENT_SUCCESS.value if is_succeed else PaymentStatus.PAYMENT_FAILED.value

    target_payment = Payment.objects.get(payment_key=payment_key)
    target_payment.status = status_value
    target_payment.save()

    _save_history(payment_key, status_value)


def _save_history(payment_key: str, status: int):
    new_payment_history = PaymentHistory(
        payment_key=payment_key,
        status=status
    )

    new_payment_history.save()
