from django.contrib import admin
from sponsor.models import Sponsor, SponsorLevel
from django_summernote.admin import SummernoteModelAdmin


class SponsorAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"
    autocomplete_fields = ('creator', 'manager_id',)
    list_display = ('creator', 'name', 'level', 'manager_name', 'manager_email', 'manager_id',
                    'submitted', 'accepted', 'paid_at',)
    list_filter = ('accepted',)
    ordering = ('-created_at',)


admin.site.register(Sponsor, SponsorAdmin)


class SponsorLevelAdmin(SummernoteModelAdmin):
    list_display = ('id', 'order', 'name', 'price', 'limit',)
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('name',)


admin.site.register(SponsorLevel, SponsorLevelAdmin)
