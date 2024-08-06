from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from program import models
from program.models import Program
from program.serializers import ProgramSerializer


class SprintListViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.filter(program_type=models.SPRINT).order_by("start_at", "title")
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        return super().get_queryset().filter(year=self.request.version or 2023)


class TutorialListViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.filter(program_type=models.TUTORIAL).order_by("start_at", "title")
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProgramSerializer

    def get_queryset(self):
        return super().get_queryset().filter(year=self.request.version or 2023)
