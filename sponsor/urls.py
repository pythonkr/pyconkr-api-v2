from django.urls import path
from rest_framework.routers import DefaultRouter

from sponsor.viewsets import SponsorViewSet

router = DefaultRouter()
router.register("", SponsorViewSet, basename="sponsor")

urlpatterns = [
    path("list/", SponsorViewSet.as_view({"get": "list"})),
    path(
        "list/<int:id>/",
        SponsorViewSet.as_view({"get": "retrieve", "put": "update"}),
    ),
]
