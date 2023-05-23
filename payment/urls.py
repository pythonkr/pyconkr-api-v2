from django.contrib import admin
from django.urls import include, path

from payment.views import PortoneWebhookApi, get__generate_payment_key


urlpatterns = [
    path("portone/webhook/", PortoneWebhookApi.as_view(), name="portone-webhook"),
    path("key/", get__generate_payment_key, name="get-payment-key"),
]
