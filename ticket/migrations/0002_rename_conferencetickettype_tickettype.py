# Generated by Django 4.1.5 on 2023-05-14 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ConferenceTicketType",
            new_name="TicketType",
        ),
    ]
