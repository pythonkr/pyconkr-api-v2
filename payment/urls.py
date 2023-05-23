from django.contrib import admin
from django.urls import include, path

from payment.views import PortoneWebhookApi


urlpatterns = [
    path("portone/webhook", PortoneWebhookApi.as_view(), name="portone-webhook"),
]
