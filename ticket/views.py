import json
import traceback
from datetime import datetime
from typing import Callable, Literal, Dict, List

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import payment.logic
from program.models import CONFERENCE, TUTORIAL, SPRINT
from .models import Ticket, TicketType
from .requests import (
    AddConferenceTicketRequest,
    CheckTicketTypeBuyableRequest,
    GetConferenceTicketTypesRequest,
    RequestParsingException,
)
from .view_models import TicketTypeViewModel

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
def get__get_ticket_types(request: HttpRequest, **kwargs) -> HttpResponse:
    """티켓 종류 목록 조회"""
    request = GetConferenceTicketTypesRequest(request, **kwargs)

    ticket_types = TicketType.objects.all()

    response: Dict[str, List[dict]] = {
        "conference": [],
        "tutorial": [],
        "sprint": [],
    }

    for ticket_type in ticket_types:
        if ticket_type.program.program_type == CONFERENCE:
            response["conference"].append(TicketTypeViewModel(ticket_type).to_dict())
        elif ticket_type.program.program_type == TUTORIAL:
            response["tutorial"].append(TicketTypeViewModel(ticket_type).to_dict())
        elif ticket_type.program.program_type == SPRINT:
            response["sprint"].append(TicketTypeViewModel(ticket_type).to_dict())

    return HttpResponse(json.dumps(response))


@request_method("GET")
@exception_wrapper
def get__check_ticket_type_buyable(
        request: HttpRequest, **kwargs
) -> HttpResponse:
    """특정 티켓 종류 구매 가능 여부 조회"""
    request = CheckTicketTypeBuyableRequest(request, **kwargs)

    ticket_type = get_object_or_404(
        TicketType, id=request.match_info.ticket_type_id
    )

    if request.querystring.username is None:
        return HttpResponse(json.dumps(ticket_type.buyable))

    try:
        user = User.objects.get(username=request.querystring.username)
    except User.DoesNotExist:
        return HttpResponse(json.dumps(ticket_type.buyable))

    bought_tickets = Ticket.objects.filter(user=user)

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
def post__add_ticket(request: HttpRequest, **kwargs) -> HttpResponse:
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

    bought_tickets = Ticket.objects.filter(user=user)
    if any(
            (
                    not bought_ticket.ticket_type.can_coexist(ticket_type)
                    for bought_ticket in bought_tickets
            )
    ):
        return HttpResponse("Duplicate day", status=400)

    ticket = Ticket.objects.create(
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
        payment_key = payment.logic.generate_payment_key(request.user, ticket_type=ticket_type)
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
