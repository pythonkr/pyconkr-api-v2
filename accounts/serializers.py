from django.contrib.auth import get_user_model

import rest_framework.serializers as serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "nickname",
            "bio"
        ]

    @staticmethod
    def get_nickname(obj: User):
        return "{}{}".format(obj.last_name, obj.first_name)

    @staticmethod
    def get_bio(obj: User):
        return obj.userext.bio
