# Generated by Django 4.1.5 on 2023-05-15 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sponsor", "0003_alter_sponsor_bank_book_file_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sponsor",
            options={
                "ordering": ["paid_at", "id"],
                "verbose_name": "후원사",
                "verbose_name_plural": "후원사 목록",
            },
        ),
        migrations.AlterModelOptions(
            name="sponsorlevel",
            options={"verbose_name": "후원사 등급", "verbose_name_plural": "후원사 등급"},
        ),
    ]