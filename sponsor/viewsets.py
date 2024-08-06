from typing import Type

from django.db.transaction import atomic

from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from sponsor.models import Patron, Sponsor, SponsorLevel, SponsorBenefit, BenefitByLevel
from sponsor.permissions import IsOwnerOrReadOnly, OwnerOnly
from sponsor.serializers import (
    PatronListSerializer,
    SponsorDetailSerializer,
    SponsorListSerializer,
    SponsorRemainingAccountSerializer,
    SponsorSerializer,
    SponsorLevelSerializer,
    SponsorBenefitSerializer,
    BenefitByLevelSerializer,
)
from sponsor.slack import send_new_sponsor_notification
from sponsor.validators import SponsorValidater



class SponsorBenefitViewSet(ModelViewSet):
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "delete"]
    serializer_class = SponsorBenefitSerializer

    def get_queryset(self):
        return SponsorBenefit.objects.all()


class SponsorLevelViewSet(ModelViewSet):
    lookup_field = "id"
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return SponsorLevel.objects.get_queryset()

    def get_serializer_class(self):
        match self.action:
            case "create_or_update_benefits" | "assign_benefits":
                return BenefitByLevelSerializer
            case _:
                return SponsorLevelSerializer

    @action(detail=False, methods=["POST"])
    def assign_benefits(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response("Already assigned", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @action(detail=True, methods=["PUT"])
    def create_or_update_benefits(self, request):
        level_id = request.data.get("level_id", None)
        benefit_id = request.data.get("benefit_id", None)
        benefit_by_level = get_object_or_404(
            BenefitByLevel, level_id=level_id, benefit_id=benefit_id
        )
        serializer = self.get_serializer(benefit_by_level, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SponsorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsOwnerOrReadOnly]  # 본인 소유만 수정 가능
    validator = SponsorValidater()

    def get_queryset(self):
        return super().get_queryset().filter(paid_at__isnull=False, level__year=self.request.version).order_by("level__order", "paid_at")

    def get_serializer_class(self):
        if self.action == "list":
            return SponsorListSerializer
        return SponsorSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.validator.assert_create(serializer.validated_data)

        new_sponsor = serializer.save()

        # slack 알림을 실패하더라도 transaction 전체를 롤백하지는 않아야 함
        # TODO 람다 외부 인터넷 접근 확인 후 활성화
        # try:
        #     send_new_sponsor_notification(new_sponsor.id, new_sponsor.name)
        # except RuntimeError as e:
        #     print(e)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs["id"]
        sponsor_data = get_object_or_404(self.get_queryset(), pk=pk)

        # 본인 소유인 경우는 모든 필드
        # 그렇지 않은 경우는 공개 가능한 필드만 응답
        serializer = (
            SponsorSerializer(sponsor_data)
            if self.check_owner_permission(request, sponsor_data)
            else SponsorDetailSerializer(sponsor_data)
        )

        return Response(serializer.data)

    def check_owner_permission(self, request, sponsor_data: Sponsor):
        return OwnerOnly.has_object_permission(
            self=Type[OwnerOnly], request=request, view=self, obj=sponsor_data
        )

    def update(self, request, *args, **kwargs):
        pk = kwargs["id"]
        sponsor_data = get_object_or_404(Sponsor, pk=pk)
        serializer = SponsorSerializer(sponsor_data, data=request.data, partial=True)

        if not self.check_owner_permission(request, sponsor_data):
            return Response(None, status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class SponsorRemainingAccountViewSet(ModelViewSet):
    serializer_class = SponsorRemainingAccountSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return SponsorLevel.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = SponsorLevel.objects.all().order_by("-price")
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class PatronListViewSet(ViewSet):
    def list(self, request):
        queryset = Patron.objects.all()
        serializer = PatronListSerializer(queryset, many=True)
        return Response(serializer.data)
