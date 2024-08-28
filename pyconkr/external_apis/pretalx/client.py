from __future__ import annotations

import logging
import traceback
import typing
import urllib.parse

import requests
from django.conf import settings

from .serializers import PretalxPaginatedSessionSerializer

logger = logging.getLogger(__name__)

RequestMethodType = typing.Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]


class PretalxException(Exception):
    pass


class PretalxClient:
    DEFAULT_TIMEOUT = 5

    def _request(self, method: RequestMethodType, endpoint: str, *args: tuple, **kwargs: dict) -> requests.Response:
        url = urllib.parse.urljoin(settings.PRETALX.API_URL, endpoint)
        request_default_headers = {
            "Authorization": f"Token {settings.PRETALX.API_KEY}",
            "Content-Type": "application/json",
        } | kwargs.pop("headers", {})
        request_default_kwargs = {
            "headers": request_default_headers,
            "timeout": self.DEFAULT_TIMEOUT,
        } | kwargs

        try:
            return requests.request(method, url, *args, **request_default_kwargs)
        except Exception as e:
            logger.error(traceback.format_exception(e))
            raise PretalxException("Pretalx API 요청에 실패했습니다.") from e

    def retrieve_sessions(self, event_name: str, only_confirmed: bool = True) -> dict:
        """세션 목록 조회"""
        endpoint = f"api/events/{event_name}/submissions" + ("?state=confirmed" if only_confirmed else "")

        try:
            result = self._request("GET", endpoint)
            result.raise_for_status()

            parsed_result = PretalxPaginatedSessionSerializer(data=result.json())
            parsed_result.is_valid(raise_exception=True)
            return parsed_result.validated_data
        except Exception as e:
            raise PretalxException("세션 목록을 가져오지 못했습니다, 잠시 후에 다시 시도해주세요.") from e


pretalx_client = PretalxClient()
