"""pyconkr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

import accounts.urls
import program.urls
import session.urls
import sponsor.urls

urlpatterns = [
    path(kwargs={"version": "2023"}, route="sponsors/", view=include(sponsor.urls)),
    path(kwargs={"version": "2023"}, route="programs/", view=include(program.urls)),
    path(kwargs={"version": "2023"}, route="sessions/", view=include(session.urls)),
    re_path(route="^(?P<version>(2023|2024))/sponsors/", view=include(sponsor.urls)),
    re_path(route="^(?P<version>(2023|2024))/programs/", view=include(program.urls)),
    re_path(route="^(?P<version>(2023|2024))/sessions/", view=include(session.urls)),
    path(route="summernote/", view=include("django_summernote.urls")),
    path(route="api-auth/", view=include("rest_framework.urls")),
    path(route="admin/", view=admin.site.urls),
    path(route="", view=include(accounts.urls)),
]

if settings.DEBUG is True:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        # Optional UI:
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
