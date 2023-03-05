from dataclasses import dataclass
from typing import Optional

from django.http import HttpRequest


class GetConferenceTicketTypesBuyableRequest:
    @dataclass
    class Querystring:
        username: Optional[str] = None

    @dataclass
    class MatchInfo:
        ...

    @dataclass
    class Data:
        ...

    def __init__(self, request: HttpRequest):
        querystring: dict = dict(request.GET)
        for k, v in querystring.items():
            if (isinstance(v, list) or isinstance(v, tuple)) and len(v) == 1:
                querystring[k] = v[0]

        self.querystring = GetConferenceTicketTypesBuyableRequest.Querystring(**querystring)

    querystring: Optional[Querystring] = None
    match_info: Optional[MatchInfo] = None
    data: Optional[Data] = None
