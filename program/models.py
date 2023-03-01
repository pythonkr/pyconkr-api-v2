from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ProgramCategory(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
        max_length=1,
        choices=(
            ("B", "Beginner"),
            ("I", "Intermediate"),
            ("E", "Experienced"),
        ),
    )

    duration = models.CharField(
        max_length=1,
        choices=(
            ("S", "25min"),
            ("L", "40min"),
        ),
    )

    language = models.CharField(
        max_length=1,
        choices=(
            ("", "---------"),
            ("K", "Korean"),
            ("E", "English"),
        ),
        default="",
    )

    category = models.ForeignKey(
        ProgramCategory, on_delete=models.SET_DEFAULT, null=True, blank=True, default=14
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
    track_num = models.IntegerField(null=True, blank=True, help_text="트랙 번호")

    def __str__(self):
        return self.title
