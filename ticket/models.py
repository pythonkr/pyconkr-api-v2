import shortuuid
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ConferenceTicketType(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    min_price = models.IntegerField(null=True, blank=True)
    desc = models.TextField(max_length=1000)
    day = models.CharField(
        max_length=10,
        choices=(
            ("SAT", "토요일"),
            ("SUN", "일요일"),
            ("WEEKEND", "토/일요일"),
        ),
    )

    def __str__(self):
        return self.name


def make_ticket_code() -> str:
    return shortuuid.uuid()


class ConferenceTicket(models.Model):
    # 구분
    ticket_type = models.ForeignKey(ConferenceTicketType, on_delete=models.RESTRICT)
    # 구매 일자
    bought_at = models.DateTimeField()
    # 사용자
    user = models.ForeignKey(User, on_delete=models.RESTRICT, db_index=True)
    # 티켓 코드
    ticket_code = models.CharField(max_length=25, default=make_ticket_code, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_code
