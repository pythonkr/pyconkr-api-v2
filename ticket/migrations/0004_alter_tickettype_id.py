# Generated by Django 4.1.5 on 2023-05-24 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_ticket_remove_tickettype_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickettype',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
