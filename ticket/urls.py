from django.urls import path, re_path

from . import views

urlpatterns = [
    path("conference-ticket-types", views.get__get_ticket_types),
    re_path(
        r"^conference-ticket-types/(?P<ticket_type_id>\w+)/check",
        views.get__check_ticket_type_buyable,
    ),
    path("conference-tickets", views.post__add_ticket),
    path("list", views.get__ticket_type_list, name="ticket-list"),
    path("<int:item_id>", views.TicketDetailView.as_view(), name="ticket-detail"),
    path("success", views.ticket_success, name="page-ticket-success"),
    path("failed", views.ticket_failed, name="page-ticket-failed"),
    path("<int:ticket_id>/refund", views.ticket_refund, name="page-ticket-refund-success"),
]
