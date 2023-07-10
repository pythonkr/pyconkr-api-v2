from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from session.models import Session
from session.serializers import SessionListSerializer, SessionSerializer


class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "head", "options"]

    def get_serializer_class(self):
        if self.action == "list":
            return SessionListSerializer
        else:
            return SessionSerializer
