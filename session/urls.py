from django.urls import include, path
from rest_framework.routers import DefaultRouter

from program.viewsets import ProposalViewSet

session_router = DefaultRouter()
session_router.register("", ProposalViewSet, basename="session")

urlpatterns = [
    path("", include(session_router.urls)),
]
