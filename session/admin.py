from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Proposal, Session, Category
from .resources import SessionResource


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "accepted",
        "difficulty",
        "duration",
        "language",
        "category",
    ]
    list_filter = ["accepted", "difficulty", "duration", "language", "category"]
    search_fields = ["title", "user__username"]


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "title",
        "host_profile_image",
        "difficulty",
        "duration",
        "language",
        "category",
    ]
    list_filter = ["difficulty", "duration", "language", "category"]
    search_fields = ["title", "user__username"]
    resource_class = SessionResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "visible"]
    list_filter = ["visible"]
    search_fields = ["name"]