from django.urls import path, re_path

from . import views

urlpatterns = [
    path("conference-ticket-types", views.get__get_conference_ticket_types),
    re_path(
        r"^conference-ticket-types/(?P<ticket_type_code>\w+)/check",
        views.get__check_conference_ticket_type_buyable,
    ),
    path("conference-tickets", views.post__add_conference_ticket),
    path("list", views.get__ticket_list, name="ticket-list"),
    path("<int:item_id>", views.TicketDetailView.as_view(), name="ticket-detail"),
    path("success", views.ticket_success, name="page-ticket-success"),
    path("failed", views.ticket_failed, name="page-ticket-failed"),
    path("<int:ticket_id>/refund", views.temp_refund),
]
