from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from program.models import Proposal, ProposalCategory


class ProposalSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            "id",
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
            "id",
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
