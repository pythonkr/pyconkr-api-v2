from django.urls import include, path
from rest_framework.routers import DefaultRouter

from session.viewsets import SessionViewSet
from session.views import get__timetable

session_router = DefaultRouter()
session_router.register("", SessionViewSet, basename="session")

urlpatterns = [
    path("", include(session_router.urls)),
    path("timetable", get__timetable),
]
