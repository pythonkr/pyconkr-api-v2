from django.db import models
from django.contrib.auth import get_user_model

from ticket.models import TicketType

User = get_user_model()


class Payment(models.Model):
    payment_key = models.CharField(max_length=32)  # TODO: uuid 처리
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    money = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class PaymentHistory(models.Model):
    payment_key = models.CharField(max_length=32)
    status = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
