import json
from datetime import datetime
from typing import Callable, Literal

from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import ConferenceTicketType, ConferenceTicket
from .requests import GetConferenceTicketTypesBuyableRequest
from .view_models import ConferenceTicketTypeViewModel

User = get_user_model()

METHOD = Literal["HEAD", "GET", "POST", "PATCH", "PUT", "DELETE"]


def request_method(method: METHOD) -> Callable:
    def decorator(func: Callable):
        @csrf_exempt
        def wrapper(*args, **kwargs):
            if args[0].method not in method:
                return HttpResponse("Method not allowed", status=405)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@request_method("GET")
def get__get_conference_ticket_types(request: HttpRequest) -> HttpResponse:
    """티켓 종류 목록 조회"""
    ticket_types = ConferenceTicketType.objects.all()

    return HttpResponse(
        json.dumps([ConferenceTicketTypeViewModel(ticket_type).to_dict() for ticket_type in ticket_types]))


@request_method("GET")
def get__check_conference_ticket_buyable(request: HttpRequest, ticket_type_code: str) -> HttpResponse:
    """특정 티켓 종류 구매 가능 여부 조회"""
    request = GetConferenceTicketTypesBuyableRequest(request)

    ticket_type = get_object_or_404(ConferenceTicketType, code=ticket_type_code)

    if request.querystring.username is None:
        return HttpResponse(json.dumps(ticket_type.buyable))

    try:
        user = User.objects.get(username=request.querystring.username)
    except User.DoesNotExist:
        return HttpResponse(json.dumps(ticket_type.buyable))

    bought_tickets = ConferenceTicket.objects.filter(user=user)

    return HttpResponse(json.dumps(ticket_type.buyable and all(
        (bought_ticket.ticket_type.can_coexist(ticket_type) for bought_ticket in bought_tickets))))


@request_method("POST")
def post__add_ticket(request: HttpRequest) -> HttpResponse:
    """티켓 결제 완료, 추가 요청"""

    data = json.loads(request.body)
    if not isinstance(data, dict):
        return HttpResponse("Invalid data", status=400)

    ticket_type = data.get("ticket_type")
    if ticket_type is None:
        return HttpResponse("Invalid ticket type", status=400)
    try:
        ticket_type = ConferenceTicketType.objects.get(code=ticket_type)
    except ConferenceTicketType.DoesNotExist:
        return HttpResponse("Invalid ticket type", status=400)

    bought_at = data.get("bought_at")
    if bought_at is None:
        return HttpResponse("Invalid bought_at", status=400)
    try:
        bought_at = datetime.strptime(bought_at, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return HttpResponse("Invalid datetime format (bought_at)", status=400)

    user = data.get("user")
    if user is None:
        return HttpResponse("Invalid user", status=400)
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        return HttpResponse("Cannot find user with user_id", status=400)

    bought_tickets = ConferenceTicket.objects.filter(user=user)
    if any((not bought_ticket.ticket_type.can_coexist(ticket_type) for bought_ticket in bought_tickets)):
        return HttpResponse("Duplicate day", status=400)

    ticket = ConferenceTicket.objects.create(
        ticket_type=ticket_type,
        bought_at=bought_at,
        user=user,
    )

    ticket.save()

    return HttpResponse(ticket.id)
