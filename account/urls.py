from django.urls import include, path

from .views import GitHubLogin, GoogleLogin, MyPage, mypage_payments

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/github/login/", GitHubLogin.as_view(), name="github_login"),
    path("auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    #path("my-page/payments", MyPage.as_view())
    path("my-page/payments/", mypage_payments)
]
