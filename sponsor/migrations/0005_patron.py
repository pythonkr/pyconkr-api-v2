# Generated by Django 4.1.5 on 2023-07-26 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sponsor", "0004_alter_sponsor_options_alter_sponsorlevel_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patron",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "total_contribution",
                    models.IntegerField(default=0, help_text="개인후원한 금액입니다."),
                ),
                (
                    "contribution_datetime",
                    models.DateTimeField(help_text="개인후원 결제한 일시입니다."),
                ),
                (
                    "contribution_message",
                    models.TextField(
                        help_text="후원메시지입니다. emoji 를 입력가능해야하고 html 태그가 들어갈 수 있습니다."
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        help_text="개인후원을 등록한 유저",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patron_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "개인후원자",
                "verbose_name_plural": "개인후원자 목록",
                "ordering": ["-total_contribution", "contribution_datetime"],
            },
        ),
    ]
