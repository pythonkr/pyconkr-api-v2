from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ticket.models import TicketType
from payment.utils import generate_payment_key


class PortoneWebhookAPI(APIView):
    def post(self, request):
        # TODO: IP Filtering
        # 52.78.100.19
        # 52.78.48.223
        # 52.78.5.241 (Webhook Test Only)

        pass

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