# Generated by Django 4.1.5 on 2023-03-14 18:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("program", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="proposal",
            options={"verbose_name": "프로그램", "verbose_name_plural": "프로그램들"},
        ),
        migrations.AlterModelOptions(
            name="proposalcategory",
            options={"verbose_name": "프로그램 카테고리", "verbose_name_plural": "프로그램 카테고리들"},
        ),
    ]
