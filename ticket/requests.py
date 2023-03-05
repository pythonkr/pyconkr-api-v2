import json
from dataclasses import dataclass

import jsons
from django.http import HttpRequest
from typing import Optional, Type, TypeVar

_T = TypeVar("_T", bound=Type)


class RequestParsingException(Exception):
    ...


def _extract_querystring(request: HttpRequest) -> dict:
    querystring: dict = dict(request.GET)
    for k, v in querystring.items():
        if (isinstance(v, list) or isinstance(v, tuple)) and len(v) == 1:
            querystring[k] = v[0]

    return querystring


@dataclass(init=False)
class GetConferenceTicketTypesRequest:
    @dataclass
    class Querystring:
        ...

    @dataclass
    class MatchInfo:
        ...

    @dataclass
    class Data:
        ...

    def __init__(self, request: HttpRequest, **kwargs):
        try:
            self.querystring = jsons.load(_extract_querystring(request), GetConferenceTicketTypesRequest.Querystring)
            self.match_info = jsons.load(kwargs, GetConferenceTicketTypesRequest.MatchInfo)
            self.data = jsons.load(json.loads(request.body) if request.body else dict(),
                                   GetConferenceTicketTypesRequest.Data)
        except Exception as e:
            raise RequestParsingException() from e

    querystring: Optional[Querystring] = None
    match_info: Optional[MatchInfo] = None
    data: Optional[Data] = None


@dataclass(init=False)
class CheckConferenceTicketTypeBuyableRequest:
    @dataclass
    class Querystring:
        username: Optional[str] = None

    @dataclass
    class MatchInfo:
        ticket_type_code: str

    @dataclass
    class Data:
        ...

    def __init__(self, request: HttpRequest, **kwargs):
        try:
            self.querystring = jsons.load(_extract_querystring(request),
                                          CheckConferenceTicketTypeBuyableRequest.Querystring)
            self.match_info = jsons.load(kwargs, CheckConferenceTicketTypeBuyableRequest.MatchInfo)
            self.data = jsons.load(json.loads(request.body) if request.body else dict(),
                                   CheckConferenceTicketTypeBuyableRequest.Data)
        except Exception as e:
            raise RequestParsingException() from e

    querystring: Optional[Querystring] = None
    match_info: Optional[MatchInfo] = None
    data: Optional[Data] = None


@dataclass(init=False)
class AddConferenceTicketRequest:
    @dataclass
    class Querystring:
        ...

    @dataclass
    class MatchInfo:
        ...

    @dataclass
    class Data:
        ticket_type: str
        bought_at: str
        username: str

    def __init__(self, request: HttpRequest, **kwargs):
        try:
            self.querystring = jsons.load(_extract_querystring(request), AddConferenceTicketRequest.Querystring)
            self.match_info = jsons.load(kwargs, AddConferenceTicketRequest.MatchInfo)
            self.data = jsons.load(json.loads(request.body) if request.body else dict(),
                                   AddConferenceTicketRequest.Data)
        except Exception as e:
            raise RequestParsingException() from e

    querystring: Optional[Querystring] = None
    match_info: Optional[MatchInfo] = None
    data: Optional[Data] = None
