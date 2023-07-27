from django.urls import path

from sponsor.viewsets import PatronListViewSet, SponsorViewSet

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
]
