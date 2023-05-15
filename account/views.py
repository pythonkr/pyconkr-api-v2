from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import payment

from allauth.account.views import LoginView, LogoutView

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

class MyPage(APIView):
    pass

@login_required
def mypage_payments(request):
    payment_list = payment.models.Payment.objects.filter(user_id=request.user)
    return render(request, 'account_mypage_payments.html',
                  context={'payment_list': payment_list})


@api_view(["POST"])
def login_api(request):

    if request.user.is_authenticated:
        return Response({"msg": "already logged in"})

    user = authenticate(
        request,
        username=request.data["username"],
        password=request.data["password"]
    )

    login(request, user)

    response_data = {
        "msg": "ok"
    }
    return Response(response_data)

@api_view(["POST"])
def logout_api(request):

    if not request.user.is_authenticated:
        return Response({"msg": "not logged in"})

    logout(request)

    response_data = {
        "msg": "ok"
    }
    return Response(response_data)

@api_view(["GET"])
def login_api_test(request):

    if request.user.is_authenticated:
        return Response({"msg": "already logged in"})

    user = authenticate(
        request,
        username="admin",
        password="admin"
    )

    login(request, user)

    response_data = {
        "msg": "ok"
    }
    return Response(response_data)
