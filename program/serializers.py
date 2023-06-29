from rest_framework import serializers

from program.models import Proposal, ProposalCategory
from accounts.serializers import UserExtSerializer


class ProposalSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    accepted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            "id",
            "title",
            "brief",
            "desc",
            "comment",
            "difficulty",
            "duration",
            "language",
            "category",
            "category_name",
            "accepted",
            "introduction",
            "video_url",
            "slide_url",
            "room_num",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance: Proposal):
        response = super().to_representation(instance)
        response["user"] = UserExtSerializer(instance.user.userext).data
        return response

    @staticmethod
    def get_category_name(obj: Proposal):
        return obj.category.name


class ProposalListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

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
            "category_name",
        ]

    @staticmethod
    def get_profile_img(obj: Proposal):
        return obj.user.userext.profile_img

    @staticmethod
    def get_category_name(obj: Proposal):
        return obj.category.name

    def to_representation(self, instance: Proposal):
        response = super().to_representation(instance)
        response["user"] = UserExtSerializer(instance.user.userext).data
        return response


class ProposalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalCategory
        fields = [
            "name",
        ]
