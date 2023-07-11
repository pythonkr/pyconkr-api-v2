from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from program.models import Program
from program import models
from program.serializers import ProgramSerializer


class SprintListViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.filter(program_type=models.SPRINT).order_by("start_at").order_by("title")
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get"]
    serializer_class = ProgramSerializer


class TutorialListViewSet(ReadOnlyModelViewSet):
    queryset = Program.objects.filter(program_type=models.TUTORIAL).order_by("start_at").order_by("title")
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get"]
    serializer_class = ProgramSerializer
