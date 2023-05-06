from django.contrib import admin

from .models import ConferenceTicket, ConferenceTicketType


class ConferenceTicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_code",
        "user",
        "ticket_type",
        "bought_at",
    )
    list_filter = ("ticket_type",)


admin.site.register(ConferenceTicket, ConferenceTicketAdmin)


class ConferenceTicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "min_price",
        "day",
    )


admin.site.register(ConferenceTicketType, ConferenceTicketTypeAdmin)
