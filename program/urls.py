from django.urls import include, path
from rest_framework.routers import DefaultRouter

from session.viewsets import SessionViewSet
from program.viewsets import SprintListViewSet, TutorialListViewSet

# TODO: 라우터 이름 변경
session_router = DefaultRouter()
session_router.register("sessions", SessionViewSet, basename="session")
session_router.register("sprint", SprintListViewSet, basename="sprint")
session_router.register("tutorial", TutorialListViewSet, basename="tutorial")

urlpatterns = [
    path("", include(session_router.urls)),     # TODO: 이전됨 -> FE 수정 후 삭제 예정
]
