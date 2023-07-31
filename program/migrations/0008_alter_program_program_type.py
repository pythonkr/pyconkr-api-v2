# Generated by Django 4.1.5 on 2023-07-31 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0007_program_profile_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="program",
            name="program_type",
            field=models.CharField(
                choices=[
                    ("CONFERENCE", "컨퍼런스"),
                    ("TUTORIAL", "튜토리얼"),
                    ("SPRINT", "스프린트"),
                    ("CHILD_CARE", "아이돌봄"),
                ],
                max_length=30,
            ),
        ),
    ]
