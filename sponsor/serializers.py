from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from sponsor.models import Sponsor, SponsorLevel


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "name",
            "desc",  # 국문/영문 모두 한 필드에 담아 제공하는 것으로 결정
            "manager_name",  # 상세에만 포함되는 필드
            "manager_email",  # 상세에만 포함되는 필드
            "business_registration_number",  # 상세에만 포함되는 필드
            "business_registration_file",  # 상세에만 포함되는 필드
            "url",
            "logo_image",
            "level",
            "id",
        ]


class SponsorListSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "name",
            "level",
            "desc",  # 국문/영문 모두 한 필드에 담아 제공하는 것으로 결정
            "url",
            "logo_image",
            "id",
        ]


class SponsorLevelSerializer(ModelSerializer):
    remaining = SerializerMethodField()

    class Meta:
        model = SponsorLevel
        fields = [
            "name",
            "price",
            "desc",
            "limit",
            "remaining",
            "id",
        ]

    def get_remaining(self, obj):
        return obj.current_remaining_number
