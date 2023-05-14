from django.db import models


class Payment(models.Model):
    payment_key = models.CharField(max_length=32)  # TODO: uuid 처리
    user_id = models.ForeignKey("", on_delete=models.PROTECT)
    money = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class PaymentHistory(models.Model):
    payment_key = models.CharField(max_length=32)
    status = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
