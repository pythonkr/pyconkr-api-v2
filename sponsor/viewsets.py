from typing import Type

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sponsor.models import Sponsor, SponsorLevel
from sponsor.permissions import IsOwnerOrReadOnly, OwnerOnly
from sponsor.serializers import (
    SponsorLevelSerializer,
    SponsorListSerializer,
    SponsorRemainingAccountSerializer,
    SponsorSerializer,
)


class SponsorViewSet(ModelViewSet):
    serializer_class = SponsorSerializer
    permission_classes = [IsOwnerOrReadOnly]  # 본인 소유만 수정가능
    http_method_names = ["get", "post"]  # 지금은 조회/등록만 가능 TODO: 추후 수정기능 추가

    def get_queryset(self):
        return Sponsor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = Sponsor.objects.filter(accepted=True).order_by("name")
        serializer = SponsorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        sponsor_data = get_object_or_404(Sponsor, pk=pk)

        # 본인 소유인 경우는 모든 필드
        # 그렇지 않은 경우는 공개 가능한 필드만 응답
        serializer = (
            SponsorSerializer(sponsor_data)
            if self.check_owner_permission(request, sponsor_data)
            else SponsorListSerializer(sponsor_data)
        )

        return Response(serializer.data)

    def check_owner_permission(self, request, sponsor_data: Sponsor):
        return OwnerOnly.has_object_permission(
            self=Type[OwnerOnly], request=request, view=self, obj=sponsor_data
        )


class SponsorLevelViewSet(ModelViewSet):
    serializer_class = SponsorLevelSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return SponsorLevel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = SponsorLevel.objects.all().order_by("-price")
        serializer = SponsorLevelSerializer(queryset, many=True)

        return Response(serializer.data)


class SponsorRemainingAccountViewSet(ModelViewSet):
    serializer_class = SponsorLevelSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return SponsorLevel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = SponsorLevel.objects.all().order_by("-price")
        serializer = SponsorRemainingAccountSerializer(queryset, many=True)

        return Response(serializer.data)
