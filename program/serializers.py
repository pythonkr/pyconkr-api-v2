from rest_framework.serializers import ModelSerializer

from program.models import Proposal, ProposalCategory


class ProposalSerializer(ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            "user",
            "title",
            "brief",
            "desc",
            "comment",
            "difficulty",
            "duration",
            "language",
            "category",
            "accepted",
            "introduction",
            "video_url",
            "slide_url",
            "room_num",
        ]


class ProposalListSerializer(ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            "title",
            "brief",
            "difficulty",
            "duration",
            "language",
            "category",
        ]


class ProposalCategorySerializer(ModelSerializer):
    class Meta:
        model = ProposalCategory
        fields = [
            "name",
        ]
