from django.contrib import admin

from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "host",
        "title",
        "room",
        "slot",
        "start_at",
        "end_at",
        "program_type",
    ]
    list_filter = ["program_type", ]
    search_fields = ["title", "host__username"]
