from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pyconkr.external_apis.pretalx.client import pretalx_client
from pyconkr.external_apis.pretalx.serializers import PretalxSessionSerializer
from session.models import Session
from session.serializers import SessionListSerializer, SessionSerializer


class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "head", "options"]

    def get_serializer_class(self):
        if self.action == "list":
            return SessionListSerializer
        return SessionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(category__year=self.request.version)

    @extend_schema(
        examples={
            200: OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(
                        name="2023년 세션 목록", value=SessionListSerializer(many=True)
                    ),
                    OpenApiExample(
                        name="2024년 이후 세션 목록 (Pretalx)",
                        value=PretalxSessionSerializer(many=True),
                    ),
                ],
            ),
        },
    )
    # cache list about 30 minutes
    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs) -> Response:
        if (
            request.version == 2023
            or request.version not in settings.PRETALX.EVENT_NAME
        ):
            return super().list(request, *args, **kwargs)

        pretalx_event_name = settings.PRETALX.EVENT_NAME[request.version]
        return Response(
            data=pretalx_client.list_sessions(
                event_name=pretalx_event_name,
                only_confirmed=not settings.DEBUG,
            )["results"],
        )

    @extend_schema(
        examples={
            200: OpenApiResponse(
                response=str,
                examples=[
                    OpenApiExample(name="2023년 세션 상세", value=SessionSerializer()),
                    OpenApiExample(
                        name="2024년 이후 세션 상세 (Pretalx)",
                        value=PretalxSessionSerializer(),
                    ),
                ],
            ),
        },
    )
    # cache each about 30 minutes
    @method_decorator(cache_page(60 * 30))
    def retrieve(self, request, *args, **kwargs) -> Response:
        if (
            request.version == 2023
            or request.version not in settings.PRETALX.EVENT_NAME
        ):
            return super().retrieve(request, *args, **kwargs)

        pretalx_event_name = settings.PRETALX.EVENT_NAME[request.version]
        return Response(
            data=pretalx_client.retrieve_session(
                event_name=pretalx_event_name,
                session_id=kwargs["pk"],
            ),
        )
