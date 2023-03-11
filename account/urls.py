from django.urls import path

from .views import GitHubLogin

urlpatterns = [
    path("github/", GitHubLogin.as_view(), name="login-github"),
]
