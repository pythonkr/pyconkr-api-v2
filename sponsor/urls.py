from django.urls import path

from sponsor.viewsets import (
    PatronListViewSet,
    SponsorViewSet,
    SponsorLevelViewSet,
    SponsorBenefitViewSet,
)

urlpatterns = [
    path("list/", SponsorViewSet.as_view({"get": "list"})),
    path(
        "list/<int:id>/",
        SponsorViewSet.as_view({"get": "retrieve", "put": "update"}),
    ),
    path(
        "patron/list/",
        PatronListViewSet.as_view({"get": "list"}),
    ),
    path(
        "levels",
        SponsorLevelViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "levels/<int:id>/",
        SponsorLevelViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
    ),
    path(
        "levels/benefits/",
        SponsorLevelViewSet.as_view(
            {"post": "assign_benefits", "put": "create_or_update_benefits"}
        ),
    ),
    path("benefits/", SponsorBenefitViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "benefits/<int:id>/",
        SponsorBenefitViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
    ),
]
