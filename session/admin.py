from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Proposal, Session
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
        "get_year",
    ]
    list_filter = ["category__year", "accepted", "difficulty", "duration", "language", "category"]
    search_fields = ["category__year", "title", "user__username"]

    @admin.display(ordering="category__year", description="Year")
    def get_year(self, obj: Proposal):
        return obj.category.year


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = [
        "id",
        "title",
        "host_profile_image",
        "host_name",
        "difficulty",
        "duration",
        "language",
        "category",
        "get_year",
    ]
    list_filter = ["category__year", "difficulty", "duration", "language", "category"]
    search_fields = ["category__year", "title", "user__username"]
    resource_class = SessionResource

    @admin.display(ordering="category__year", description="Year")
    def get_year(self, obj: Session):
        return obj.category.year


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["year", "id", "name", "visible"]
    list_filter = ["year", "visible"]
    search_fields = ["year", "name"]
