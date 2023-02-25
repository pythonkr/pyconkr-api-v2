from django.contrib import admin

from status.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "open_at", "close_at")
    list_editable = (
        "open_at",
        "close_at",
    )
    ordering = ("open_at",)
    search_fields = ("name",)


admin.site.register(Status, StatusAdmin)
