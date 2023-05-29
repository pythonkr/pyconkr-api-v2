from django.contrib import admin
from django.urls import include, path

from payment.views import PortoneWebhookApi, post__generate_payment_key, PaymentSuccessApi, post__cancel_payment

urlpatterns = [
    path("portone/webhook/", PortoneWebhookApi.as_view(), name="portone-webhook"),
    path("key/", post__generate_payment_key, name="get-payment-key"),
    path("success/", PaymentSuccessApi.as_view(), name="payment-success"),
    path("calcel/", post__cancel_payment, name="cancel-payment"),
]
