from rest_framework.response import Response

from program.models import Session


def get__timetable(request):
    response = dict()

    response["day1"] = Session.objects.filter()

    response["day2"] = Session.objects.filter()

    return Response(data=response)
