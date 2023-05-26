from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Payment(models.Model):
    payment_key = models.CharField(max_length=32)  # TODO: uuid 처리
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    ticket_type = models.ForeignKey("ticket.TicketType", on_delete=models.PROTECT)
    money = models.IntegerField()
    status = models.IntegerField(
        choices=(
            (1, "결제 전"),
            (2, "결제 실패"),
            (3, "결제 성공"),
            (4, "환불 실패"),
            (5, "환불 완료"),
        )
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class PaymentHistory(models.Model):
    payment_key = models.CharField(max_length=32)
    status = models.IntegerField(
        choices=(
            (1, "결제 전"),
            (2, "결제 실패"),
            (3, "결제 성공"),
            (4, "환불 실패"),
            (5, "환불 완료"),
        )
    )
    is_webhook = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
