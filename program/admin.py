from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Program
from .resources import ProgramResource


@admin.register(Program)
class ProgramAdmin(ImportExportModelAdmin):
    list_display = [
        "year",
        "id",
        "host",
        "profile_img",
        "title",
        "room",
        "slot",
        "start_at",
        "end_at",
        "program_type",
    ]
    list_filter = ["year", "program_type"]
    search_fields = ["title", "host__username"]
    resource_class = ProgramResource
