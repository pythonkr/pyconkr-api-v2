from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from sponsor.serializers import (
    SponsorSerializer,
    SponsorListSerializer,
)
from sponsor.models import Sponsor


class SponsorViewSet(ReadOnlyModelViewSet):
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 로그인된 사용자에게만 허용

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

        serializer = SponsorSerializer(sponsor_data)
        return Response(serializer.data)
