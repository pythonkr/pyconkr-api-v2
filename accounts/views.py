from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.logics import get_basic_auth_token


class IdLogin(LoginView):
    template_name = "account/login.html"
    success_url = "/"


class Logout(LogoutView):
    template_name = "account/logout.html"


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.OAUTH_GITHUB_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.OAUTH_GOOGLE_CALLBACK_URL
    client_class = OAuth2Client


@api_view(["POST"])
def login_api(request):
    if request.user.is_authenticated:
        return Response({"msg": "already logged in"})

    user = authenticate(
        request,
        username=request.data["username"],
        password=request.data["password"]
    )

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    response_data = {
        "msg": "ok",
        "basic_auth_token": get_basic_auth_token(request.data["username"], request.data["password"])
    }

    return Response(response_data)


@api_view(["POST"])
def logout_api(request):
    if not request.user.is_authenticated:
        return Response({"msg": "not logged in"})

    logout(request)
    return Response({"msg": "ok"})
