from django.contrib.auth import get_user_model

import rest_framework.serializers as serializers
from accounts.models import UserExt

User = get_user_model()


class UserExtSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = UserExt
        fields = [
            "nickname",
            "bio",
            "profile_img",
        ]

    @staticmethod
    def get_nickname(obj: UserExt):
        return "{}{}".format(obj.user.last_name, obj.user.first_name)
