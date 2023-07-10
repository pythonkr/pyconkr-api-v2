from django.contrib import admin

from .models import Proposal, Session, Category


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
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "difficulty",
        "duration",
        "language",
        "category",
    ]
    list_filter = ["difficulty", "duration", "language", "category"]
    search_fields = ["title", "user__username"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "visible"]
    list_filter = ["visible"]
    search_fields = ["name"]