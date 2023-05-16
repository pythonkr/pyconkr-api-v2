from django.urls import include, path
from .views import GitHubLogin, GoogleLogin, mypage_payments
from .views import IdLogin, Logout
from .views import login_api, logout_api
from . import views
from .views import GitHubLogin, GoogleLogin

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("accounts/login/", IdLogin.as_view(), name='account_login'),
    path("accounts/email/", IdLogin.as_view(), name='account_email'),
    path("accounts/logout/", Logout.as_view(), name='account_logout'),
    path("accounts/signup/", IdLogin.as_view(), name="account_signup"),
    path("auth/github/login/", GitHubLogin.as_view(), name="github_login"),
    path("auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    path("my-page/payments/", mypage_payments),

    # Endpoints for Session Based Login
    path("api/login/", login_api, name="login-api"),
    path("api/logout/", logout_api, name="logout-api"),

    # Google Social Login
    path('google/login/', views.google_login, name='google_login'),
    path('google/login/callback/', views.google_callback, name="google_callback"),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_finish'),
]
