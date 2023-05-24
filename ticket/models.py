from __future__ import annotations

import shortuuid
from constance import config
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TicketType(models.Model):
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
    # program = models.ForeignKey()     # TODO
    is_refundable = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def buyable(self) -> bool:
        """잔여 수량이 있는지"""
        sat_ticket_count = Ticket.objects.filter(
            models.Q(ticket_type__day="SAT") | models.Q(ticket_type__day="WEEKEND")
        ).filter(is_refunded=False).count()
        sun_ticket_count = Ticket.objects.filter(
            models.Q(ticket_type__day="SUN") | models.Q(ticket_type__day="WEEKEND")
        ).filter(is_refunded=False).count()

        can_buy_sat_ticket = sat_ticket_count < config.CONFERENCE_PARTICIPANT_COUNT_SAT
        can_buy_sun_ticket = sun_ticket_count < config.CONFERENCE_PARTICIPANT_COUNT_SUN

        if self.day == "SAT":
            return can_buy_sat_ticket
        elif self.day == "SUN":
            return can_buy_sun_ticket
        elif self.day == "WEEKEND":
            return can_buy_sat_ticket and can_buy_sun_ticket
        else:
            raise ValueError(f"{self.day} is not valid day.")

    def can_coexist(self, other: TicketType) -> bool:
        if self.day == "SAT" and other.day == "SUN":
            return True
        if self.day == "SUN" and other.day == "SAT":
            return True

        return False


def make_ticket_code() -> str:
    return shortuuid.uuid()


class Ticket(models.Model):
    # 구분
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.RESTRICT, db_index=True
    )
    # 구매 일자
    bought_at = models.DateTimeField()
    # 사용자
    user = models.ForeignKey(User, on_delete=models.RESTRICT, db_index=True)
    # 티켓 코드
    ticket_code = models.CharField(
        max_length=25, default=make_ticket_code, unique=True, db_index=True
    )
    # 결제 정보
    payment = models.ForeignKey("payment.Payment", on_delete=models.PROTECT, null=True)
    is_refunded = models.BooleanField(default=False)
    refunded_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_code
