from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.views import APIView

import payment


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
