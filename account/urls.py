from django.urls import include, path

from .views import GitHubLogin, GoogleLogin, MyPage

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/github/login/", GitHubLogin.as_view(), name="github_login"),
    path("auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    path("my-page/payments", MyPage.as_view())
]
