from rest_framework.routers import DefaultRouter

from sponsor.viewsets import *


def get_router():
    router = DefaultRouter()
    router.register("prospectus", SponsorLevelViewSet, basename="prospectus")
    router.register("", SponsorViewSet, basename="sponsor")

    return router
