from django.contrib import admin
from django.urls import include, path

from payment.views import get__generate_payment_key

urlpatterns = [
    path("payment-key/", get__generate_payment_key, name="generate-payment-key"),
]
