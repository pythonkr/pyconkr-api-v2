from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CONFERENCE = "CONFERENCE"
TUTORIAL = "TUTORIAL"
SPRINT = "SPRINT"
CHILDCARE = "CHILDCARE"


class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    host = models.CharField(max_length=100)  # TODO User로?
    year = models.IntegerField(default=2023)
    title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=1000)
    desc = models.CharField(max_length=4000)
    room = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        choices=(
            ("101", "101"),
            ("102", "102"),
            ("103", "103"),
            ("104", "104"),
            ("105", "105"),
            ("201", "201"),
            ("202", "202"),
            ("203", "203"),  # TODO 2층 호실 추가 필요
        ),
    )
    slot = models.IntegerField(null=True, blank=True, help_text="최대 참가 가능 인원 수")
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    program_type = models.CharField(
        max_length=30,
        choices=(
            (CONFERENCE, "컨퍼런스"),
            (TUTORIAL, "튜토리얼"),
            (SPRINT, "스프린트"),
            (CHILDCARE, "아이돌봄"),
        ),
    )
    profile_img = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = "프로그램들"

    def __str__(self):
        return self.title
