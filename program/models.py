from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ProposalCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "프로그램 카테고리"
        verbose_name_plural = "프로그램 카테고리들"

    def __str__(self):
        return self.name


class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255)
    brief = models.TextField(max_length=1000, help_text="리뷰용: 발표에 대한 간단한 설명.")
    desc = models.TextField(max_length=4000, help_text="리뷰용: 발표에 대한 자세한 설명")
    comment = models.TextField(
        max_length=4000, null=True, blank=True, help_text="리뷰용: 파준위에게 전하고 싶은 말"
    )

    difficulty = models.CharField(
        max_length=15,
        choices=(
            ("BEGINNER", "Beginner"),
            ("INTERMEDIATE", "Intermediate"),
            ("EXPERIENCED", "Experienced"),
        ),
    )

    duration = models.CharField(
        max_length=15,
        choices=(
            ("SHORT", "25min"),
            ("LONG", "40min"),
        ),
    )

    language = models.CharField(
        max_length=15,
        choices=(
            ("", "---------"),
            ("KOREAN", "Korean"),
            ("ENGLISH", "English"),
        ),
        default="",
    )

    category = models.ForeignKey(
        ProposalCategory,
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default=14,
    )
    accepted = models.BooleanField(default=False)
    introduction = models.TextField(
        max_length=2000,
        null=True,
        blank=True,
        help_text="발표 소개 페이지에 들어가는 내용입니다. 변경 사항은 최대 60분 이내에 적용됩니다.",
    )
    video_url = models.CharField(
        max_length=255, null=True, blank=True, help_text="발표 영상 URL"
    )
    slide_url = models.CharField(
        max_length=255, null=True, blank=True, help_text="발표 자료 URL"
    )
    room_num = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        help_text="발표장소",
        choices=(
            ("101", "101"),
            ("102", "102"),
            ("103", "103"),
            ("104", "104"),
            ("105", "105"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "프로그램"
        verbose_name_plural = "프로그램들"

    def __str__(self):
        return self.title


CONFERENCE = "CONFERENCE"
TUTORIAL = "TUTORIAL"
SPRINT = "SPRINT"


class Program(models.Model):
    id = models.UUIDField(primary_key=True)
    host = models.CharField(max_length=100)  # TODO User로?
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
        ),
    )

    def __str__(self):
        return self.title
