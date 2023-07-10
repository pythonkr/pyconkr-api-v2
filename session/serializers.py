from rest_framework import serializers

from session.models import Session, Category, Session
from accounts.serializers import UserExtSerializer


class SessionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    accepted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Session
        fields = [
            "id",
            "title",
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

    def to_representation(self, instance: Session):
        response = super().to_representation(instance)
        response["user"] = UserExtSerializer(instance.user.userext).data
        return response

    @staticmethod
    def get_category_name(obj: Session):
        return obj.category.name


class SessionListSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = [
            "id",
            "title",
            "introduction",
            "difficulty",
            "duration",
            "language",
            "category",
            "category_name",
        ]

    @staticmethod
    def get_profile_img(obj: Session):
        return obj.user.userext.profile_img

    @staticmethod
    def get_category_name(obj: Session):
        return obj.category.name

    def to_representation(self, instance: Session):
        response = super().to_representation(instance)

        if instance.user is not None:
            response["user"] = UserExtSerializer(instance.user.userext).data
        else:
            response["user"] = None

        return response


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
        ]
