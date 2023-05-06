from django.contrib import admin

from .models import Proposal, ProposalCategory


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


@admin.register(ProposalCategory)
class ProposalCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "visible"]
    list_filter = ["visible"]
    search_fields = ["name"]
