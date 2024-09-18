from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from import_export.admin import ImportExportModelAdmin

from sponsor.models import Sponsor, SponsorLevel, Patron, SponsorBenefit, BenefitByLevel


class SponsorAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"
    autocomplete_fields = (
        "creator",
        "manager_id",
    )
    list_display = (
        "name",
        "level",
        "manager_name",
        "manager_email",
        "manager_id",
        "submitted",
        "accepted",
        "paid_at",
    )
    list_filter = ("accepted", "submitted")
    ordering = ("-created_at",)


admin.site.register(Sponsor, SponsorAdmin)


class SponsorLevelAdmin(SummernoteModelAdmin):
    list_display = (
        "id",
        "order",
        "name",
        "price",
        "limit",
        "year",
    )
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("name", "year")


admin.site.register(SponsorLevel, SponsorLevelAdmin)


class SponsorBenefitAdmin(SummernoteModelAdmin):
    list_display = (
        "id",
        "name",
        "desc",
        "unit",
        "year",
        "is_countable",
    )
    ordering = ("-year", "id")
    search_fields = ("name", "year")
    list_editable = ("unit", "is_countable")


admin.site.register(SponsorBenefit, SponsorBenefitAdmin)


class BenefitByLevelAdmin(SummernoteModelAdmin):
    list_display = ("id", "benefit_id", "level_id", "offer")
    list_editable = ("offer",)


admin.site.register(BenefitByLevel, BenefitByLevelAdmin)


class PatronAdmin(SummernoteModelAdmin, ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "total_contribution",
    )
    ordering = ("total_contribution",)
    search_fields = ("name",)


admin.site.register(Patron, PatronAdmin)
