from rest_framework import serializers

from program.models import Proposal, ProposalCategory


class ProposalSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    accepted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Proposal
        fields = [
            "id",
            "username",
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

    @staticmethod
    def get_username(obj: Proposal):
        return "{}{}".format(obj.user.last_name, obj.user.first_name)

    @staticmethod
    def get_category_name(obj: Proposal):
        return obj.category.name



class ProposalListSerializer(serializers.ModelSerializer):
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

    @staticmethod
    def get_profile_img(obj: Proposal):
        return obj.user.userext.profile_img


class ProposalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalCategory
        fields = [
            "name",
        ]
