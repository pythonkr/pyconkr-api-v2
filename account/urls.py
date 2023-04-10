from django.urls import include, path

from .views import GitHubLogin

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/github/login/", GitHubLogin.as_view(), name="github_login"),
]
