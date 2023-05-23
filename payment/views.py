from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket.models import TicketType
from payment.logic import generate_payment_key
from payment.models import Payment

from django.conf import settings


class PortoneWebhookApi(APIView):
    def post(self, request):
        portone_ips = [
            "52.78.100.19",
            "52.78.48.223",
            "52.78.5.241"   # (Webhook Test Only)
        ]

        if settings.DEBUG is False and request.META.get("REMOTE_ADDR") not in portone_ips:
            raise ValueError("Not Allowed IP")

        target_payment = Payment.objects.get(payment_key=request.data["merchant_uid"])

        if request.data["status "] != "paid":
            raise ValueError("결제 승인건 이외의 요청")

        dto = {
            "msg": "ok",
            "merchant_uid": request.data["merchant_uid"]
        }

        return Response(dto)


@api_view(["GET"])
def get__generate_payment_key(request):

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
