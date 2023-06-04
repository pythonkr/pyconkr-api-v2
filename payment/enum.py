from enum import Enum


class PaymentStatus(Enum):
    BEFORE_PAYMENT = 1
    PAYMENT_FAILED = 2
    PAYMENT_SUCCESS = 3
    REFUND_FAILED = 4
    REFUND_SUCCESS = 5