from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket.models import TicketType
from payment.logic import generate_payment_key
from payment.models import Payment


class PortoneWebhookApi(APIView):
    def post(self, request):
        # TODO: IP Filtering
        # 52.78.100.19
        # 52.78.48.223
        # 52.78.5.241 (Webhook Test Only)

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
        "payment_key": payment_key
    }

    return Response()