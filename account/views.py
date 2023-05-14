from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView

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
    pass

@login_required
def mypage_payments(request):
    ticket_list = Ticket.objects.filter(user=request.user)
    return render(request, 'account_mypage_payments.html',
                  context={'ticket_list': ticket_list})
