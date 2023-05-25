from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from payment import enum
from ticket.models import TicketType
from payment.logic import generate_payment_key
from payment.models import Payment, PaymentHistory

from django.conf import settings


class PortoneWebhookApi(APIView):
    @transaction.atomic
    def post(self, request):
        portone_ips = [
            "52.78.100.19",
            "52.78.48.223",
            "52.78.5.241"   # (Webhook Test Only)
        ]

        if settings.DEBUG is False and request.META.get("REMOTE_ADDR") not in portone_ips:
            raise ValueError("Not Allowed IP")

        payment_key = request.data["merchant_uid"]

        target_payment = Payment.objects.get(payment_key=payment_key)
        target_payment.status = enum.PaymentStatus.PAYMENT_SUCCESS.value
        target_payment.save()

        payment_history = PaymentHistory(
            payment_key=payment_key,
            status=enum.PaymentStatus.PAYMENT_SUCCESS.value,
            is_webhook=True
        )
        payment_history.save()

        if request.data["status"] != "paid":
            raise ValueError("결제 승인건 이외의 요청")

        dto = {
            "msg": "ok",
            "merchant_uid": request.data["merchant_uid"]
        }

        return Response(dto)


class PaymentSuccessApi(APIView):
    def post(self, request):
        if not request.is_authenticated:
            return Response({"msg": "not logged in user"}, status=400)

        payment_key = request.data["merchant_uid"]

        payment_history = PaymentHistory(
            payment_key=payment_key,
            status=enum.PaymentStatus.PAYMENT_SUCCESS.value,
            is_webhook=False
        )
        payment_history.save()

        dto = {
            "msg": "ok",
            "merchant_uid": request.data["merchant_uid"]
        }

        return Response(dto)


@api_view(["POST"])
def post__generate_payment_key(request):

    request_ticket_type = TicketType.objects.get(id=request.data["ticket_type"])

    payment_key = generate_payment_key(
        user=request.user,
        ticket_type=request_ticket_type
    )

    response_data = {
        "msg": "ok",
        "payment_key": payment_key,
        "price": request_ticket_type.price
    }

    return Response(response_data)
