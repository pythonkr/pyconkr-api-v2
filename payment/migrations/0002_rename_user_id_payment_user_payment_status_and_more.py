# Generated by Django 4.1.5 on 2023-05-15 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0002_rename_conferencetickettype_tickettype"),
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="user_id",
            new_name="user",
        ),
        migrations.AddField(
            model_name="payment",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "결제 전"),
                    (2, "결제 실패"),
                    (3, "결제 성공"),
                    (4, "환불 실패"),
                    (5, "환불 완료"),
                ],
                default=0,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="payment",
            name="ticket_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="ticket.tickettype",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="paymenthistory",
            name="status",
            field=models.IntegerField(
                choices=[
                    (1, "결제 전"),
                    (2, "결제 실패"),
                    (3, "결제 성공"),
                    (4, "환불 실패"),
                    (5, "환불 완료"),
                ]
            ),
        ),
    ]
