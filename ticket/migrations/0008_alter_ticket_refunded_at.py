# Generated by Django 4.1.5 on 2023-06-01 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_alter_tickettype_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='refunded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]