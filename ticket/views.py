from django.http import HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404

from .models import ConferenceTicketType


def get__get_conference_ticket_types(request: HttpRequest) -> HttpResponse:
    """티켓 종류 목록 조회"""
    ...


def get__check_conference_ticket_buyable(request: HttpRequest, ticket_type_code: str) -> HttpResponse:
    """특정 티켓 종류 구매 가능 여부 조회"""
    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    ticket_type = get_object_or_404(ConferenceTicketType, code=ticket_type_code)

    return HttpResponse(ticket_type.buyable)


def post__add_ticket(request: HttpRequest) -> HttpResponse:
    """티켓 결제 완료, 추가 요청"""
    ...
