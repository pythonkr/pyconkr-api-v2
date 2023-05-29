from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from functional import seq

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from account.logics import get_basic_auth_token
from account.view_models import UserTicketInfo
from ticket.models import Ticket

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
    def get(self, request):
        dto = {
            "ticket": self.get_ticket_info(request)
            # "session": None,        # TODO 세션
            # "sponsor": None,        # TODO 후원사
            # "user_info": None       # TODO 사용자 정보
        }

        return Response(dto)

    def get_ticket_info(self, request) -> list:
        all_tickets = Ticket.objects.filter(
            user=request.user,
            is_refunded=False
        )

        return list(
            seq(all_tickets)
            .map(UserTicketInfo)
            .map(lambda info: info.to_dict())
        )


@login_required
def mypage_payments(request):
    ticket_list = Ticket.objects.filter(user=request.user)
    return render(request, 'account_mypage_payments.html',
                  context={'ticket_list': ticket_list})


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

    response_data = {
        "msg": "ok"
    }
    return Response(response_data)
