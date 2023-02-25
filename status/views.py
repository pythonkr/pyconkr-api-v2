import datetime

from django.shortcuts import get_object_or_404
from pytz import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from status.models import Status


class StatusView(APIView):
    def get(self, request, name: str):
        status = get_object_or_404(Status, name=name)
        now = datetime.datetime.now(tz=timezone("Asia/Seoul"))

        flag = None

        if status.open_at < now < status.close_at:
            flag = True
        else:
            flag = False

        return Response({"name": name, "open": flag})
