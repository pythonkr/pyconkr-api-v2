from rest_framework.views import APIView


class PortoneWebhookAPI(APIView):
    def post(self, request):
        # TODO: IP Filtering
        # 52.78.100.19
        # 52.78.48.223
        # 52.78.5.241 (Webhook Test Only)

        pass

