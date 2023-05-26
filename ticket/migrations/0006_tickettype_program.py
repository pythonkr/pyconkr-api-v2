# Generated by Django 4.1.5 on 2023-05-24 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0003_program'),
        ('ticket', '0005_alter_tickettype_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettype',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='program.program'),
        ),
    ]