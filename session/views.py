import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from session.models import Session
from session.serializers import SessionSerializer


@api_view(["GET"])
def get__timetable(request):
    response = dict()

    MONTH = 8
    FIRST_DAY = 12
    SECOND_DAY = 13

    response["day1"] = SessionSerializer(
        Session.objects.filter(
            start_at__month=MONTH,
            start_at__day=FIRST_DAY
        ),
        many=True
    ).data

    response["day2"] = SessionSerializer(
        Session.objects.filter(
            start_at__month=MONTH,
            start_at__day=SECOND_DAY
        ),
        many=True
    ).data

    return Response(data=response)
