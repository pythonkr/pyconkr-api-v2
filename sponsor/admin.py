from django.contrib import admin
from sponsor.models import Sponsor, SponsorLevel


class SponsorAdmin(SummernoteModelAdmin):
    formfield_overrides = {models.TextField: {
        'widget': SummernoteWidgetWithCustomToolbar}}
    autocomplete_fields = ('creator', 'manager_id',)
    list_display = ('creator', 'name', 'level', 'manager_name', 'manager_email', 'manager_id',
                    'submitted', 'accepted', 'paid_at',)
    list_filter = ('accepted',)
    ordering = ('-created_at',)


admin.site.register(Sponsor, SponsorAdmin)


class SponsorLevelAdmin(SummernoteModelAdmin):
    list_display = ('id', 'order', 'name', 'slug', 'price', 'limit',)
    list_editable = ('order', 'slug',)
    ordering = ('order',)
    search_fields = ('name',)


admin.site.register(SponsorLevel, SponsorLevelAdmin)
