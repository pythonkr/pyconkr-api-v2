from rest_framework.viewsets import ModelViewSet

from program.models import Proposal
from program.serializers import ProposalListSerializer, ProposalSerializer


class ProposalViewSet(ModelViewSet):
    queryset = Proposal.objects.all()
    http_method_names = ["get", "head", "options"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProposalListSerializer
        else:
            return ProposalSerializer
