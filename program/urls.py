from django.urls import include, path
from rest_framework.routers import DefaultRouter

from program.viewsets import ProposalViewSet

router = DefaultRouter()
router.register("", ProposalViewSet, basename="program")

urlpatterns = [
    path("", include(router.urls)),
]
