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
            "created_at",
            "updated_at",
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
            "created_at",
            "updated_at",
        ]


class ProposalCategorySerializer(ModelSerializer):
    class Meta:
        model = ProposalCategory
        fields = [
            "name",
        ]
