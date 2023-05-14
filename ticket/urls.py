from django.urls import path, re_path

from . import views

urlpatterns = [
    path("conference-ticket-types", views.get__get_conference_ticket_types),
    re_path(
        r"^conference-ticket-types/(?P<ticket_type_code>\w+)/check",
        views.get__check_conference_ticket_type_buyable,
    ),
    path("conference-tickets", views.post__add_conference_ticket),
    path("list", views.temp),
    path("<int:item_id>", views.temp),
    path("success", views.temp),
    path("failed", views.temp),
    path("<int:ticket_id>/refund", views.temp_refund),
]
