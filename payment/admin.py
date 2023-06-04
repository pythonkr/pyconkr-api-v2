from django.contrib import admin

from .models import Payment, PaymentHistory

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    pass


class PaymentHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentHistory, PaymentHistoryAdmin)
