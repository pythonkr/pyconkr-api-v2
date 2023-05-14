import json
import traceback
from datetime import datetime
from typing import Callable, Literal

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import ConferenceTicket, TicketType
from .requests import (
    AddConferenceTicketRequest,
    CheckConferenceTicketTypeBuyableRequest,
    GetConferenceTicketTypesRequest,
    RequestParsingException,
)
from .view_models import ConferenceTicketTypeViewModel

import payment.utils

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


def exception_wrapper(func: Callable[[HttpRequest, ...], HttpResponse]):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestParsingException:
            traceback.print_exc()
            print(f"{args=}")
            print(f"{kwargs=}")
            return HttpResponse("Invalid request", status=400)
        except (Exception,):
            print(f"{args=}")
            print(f"{kwargs=}")
            traceback.print_exc()
            return HttpResponse(status=500)

    return wrapper


@request_method("GET")
@exception_wrapper
def get__get_conference_ticket_types(request: HttpRequest, **kwargs) -> HttpResponse:
    """티켓 종류 목록 조회"""
    request = GetConferenceTicketTypesRequest(request, **kwargs)

    ticket_types = TicketType.objects.all()

    return HttpResponse(
        json.dumps(
            [
                ConferenceTicketTypeViewModel(ticket_type).to_dict()
                for ticket_type in ticket_types
            ]
        )
    )


@request_method("GET")
@exception_wrapper
def get__check_conference_ticket_type_buyable(
    request: HttpRequest, **kwargs
) -> HttpResponse:
    """특정 티켓 종류 구매 가능 여부 조회"""
    request = CheckConferenceTicketTypeBuyableRequest(request, **kwargs)

    ticket_type = get_object_or_404(
        TicketType, code=request.match_info.ticket_type_code
    )

    if request.querystring.username is None:
        return HttpResponse(json.dumps(ticket_type.buyable))

    try:
        user = User.objects.get(username=request.querystring.username)
    except User.DoesNotExist:
        return HttpResponse(json.dumps(ticket_type.buyable))

    bought_tickets = ConferenceTicket.objects.filter(user=user)

    return HttpResponse(
        json.dumps(
            ticket_type.buyable
            and all(
                (
                    bought_ticket.ticket_type.can_coexist(ticket_type)
                    for bought_ticket in bought_tickets
                )
            )
        )
    )


@request_method("POST")
@exception_wrapper
def post__add_conference_ticket(request: HttpRequest, **kwargs) -> HttpResponse:
    """티켓 결제 완료, 추가 요청"""
    request = AddConferenceTicketRequest(request)

    data = request.data

    ticket_type = data.ticket_type
    if ticket_type is None:
        return HttpResponse("Invalid ticket type", status=400)
    try:
        ticket_type = TicketType.objects.get(code=ticket_type)
    except TicketType.DoesNotExist:
        return HttpResponse("Invalid ticket type", status=400)

    bought_at = data.bought_at
    if bought_at is None:
        return HttpResponse("Invalid bought_at", status=400)
    try:
        bought_at = datetime.strptime(bought_at, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return HttpResponse("Invalid datetime format (bought_at)", status=400)

    username = data.username
    if username is None:
        return HttpResponse("Invalid username", status=400)
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Cannot find user with user_id", status=400)

    bought_tickets = ConferenceTicket.objects.filter(user=user)
    if any(
        (
            not bought_ticket.ticket_type.can_coexist(ticket_type)
            for bought_ticket in bought_tickets
        )
    ):
        return HttpResponse("Duplicate day", status=400)

    ticket = ConferenceTicket.objects.create(
        ticket_type=ticket_type,
        bought_at=bought_at,
        user=user,
    )

    ticket.save()

    return HttpResponse(ticket.id)


def get__ticket_list(request):
    all_types = TicketType.objects.all()

    dto = {
        "ticket_items": all_types,
    }

    return render(request, "ticket-list.html", dto)


class TicketDetailView(View):
    def get(self, request, item_id: int):
        ticket_type = TicketType.objects.get(id=item_id)
        payment_key = payment.utils.generate_payment_key(request.user, ticket_type=ticket_type)
        user = request.user

        dto = {
            "ticket_type": ticket_type,
            "payment_key": payment_key,
            "user_name": user.last_name + user.first_name
        }

        return render(request, "ticket-detail.html", dto)


def ticket_success(request):
    return render(request, "ticket-success.html")


def ticket_failed(request):
    return render(request, "ticket-failed.html")


def ticket_refund(request, ticket_id):
    return render(request, "ticket-refund-success.html")
