from django.urls import include, path

from .views import GitHubLogin, GoogleLogin, IdLogin, Logout, login_api, logout_api

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("accounts/login/", IdLogin.as_view(), name='account_login'),
    path("accounts/email/", IdLogin.as_view(), name='account_email'),
    path("accounts/logout/", Logout.as_view(), name='account_logout'),
    path("accounts/signup/", IdLogin.as_view(), name="account_signup"),
    path("auth/github/login/", GitHubLogin.as_view(), name="github_login"),
    path("auth/google/login/", GoogleLogin.as_view(), name="google_login"),

    # Endpoints for Seesion Based Login
    path("api/login/", login_api, name="login-api"),
    path("api/logout/", logout_api, name="logout-api"),
]
