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
from ticket.models import Ticket
from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.models import SocialAccount, SocialApp
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework.response import Response
import requests
from rest_framework import status
from json.decoder import JSONDecodeError
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
import os

User = get_user_model()
client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")


class IdLogin(LoginView):
    template_name = "account/login.html"
    success_url = "/"


class Logout(LogoutView):
    template_name = "account/logout.html"


class MyPage(APIView):
    pass


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.OAUTH_GITHUB_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.OAUTH_GOOGLE_CALLBACK_URL
    client_class = OAuth2Client


@login_required
def mypage_payments(request):
    ticket_list = Ticket.objects.filter(user=request.user)
    return render(
        request, "account_mypage_payments.html", context={"ticket_list": ticket_list}
    )


@api_view(["POST"])
def login_api(request):
    if request.user.is_authenticated:
        return Response({"msg": "already logged in"})

    user = authenticate(
        request, username=request.data["username"], password=request.data["password"]
    )

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    response_data = {"msg": "ok"}
    return Response(response_data)


@api_view(["POST"])
def logout_api(request):
    if not request.user.is_authenticated:
        return Response({"msg": "not logged in"})

    logout(request)

    response_data = {"msg": "ok"}
    return Response(response_data)


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={settings.OAUTH_GOOGLE_CALLBACK_URL}&scope={scope}"
    )


def google_callback(request):
    # "콜백", request
    code = request.GET.get("code")

    # "구글 콜백 클라이언트 아이디:", client_id, "클라이언트 시크릿:", client_secret, "코드:", code)
    """
    Access Token Request
    """
    # "구글 콜백 URI: ", settings.OAUTH_GOOGLE_CALLBACK_URL
    # "인증 주소:", f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={settings.OAUTH_GOOGLE_CALLBACK_URL}"
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={settings.OAUTH_GOOGLE_CALLBACK_URL}"
    )
    token_req_json = token_req.json()
    print("토큰 리퀘token_req", token_req)
    error = token_req_json.get("error")
    # "콜백 토큰 리퀘스트 제이슨: token_req_json
    if error is not None:
        # "JSON 디코드 에러"
        raise JSONDecodeError(error)
    # 액세스 토큰
    access_token = token_req_json.get("access_token")
    # 아이디 토큰
    id_token = token_req_json.get("id_token")
    print("액세스 토큰", access_token)
    print("아이디 토큰", id_token)

    """
    Profile Request
    """

    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={"access_token": access_token, "id_token": id_token},
    )
    print("유저 인포 리스폰스", user_info_response)
    user_info = user_info_response.json()
    print("유저 인포", user_info)

    email = user_info["email"]
    print("이메일", email)

    """
    Signup or Signin Request
    """
    try:
        # 기존 유저 있음
        user = User.objects.get(email=email)

        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        # 소셜 유저: social_user
        if social_user is None:
            # 소셜 유저 없음
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            # 구글이 아님
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code, "id_token": id_token}
        # 넘어온 데이터 data
        print("유저 토큰 데이터: ", data)

        accept = requests.post(f"http://localhost:8000/google/login/finish/", data=data)
        accept_status = accept.status_code
        print("억셉트: ", accept)
        print("피니쉬 억셉트 스테이터스: ", accept_status)
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code, "id_token": id_token}
        print("노 유저 토큰 데이터: ", data)
        accept = requests.post(f"http://localhost:8000/google/login/finish/", data=data)

        accept_status = accept.status_code

        print("노 유저 억셉트: ", accept)
        print("피니쉬 억셉트 스테이터스: ", accept_status)
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json)
