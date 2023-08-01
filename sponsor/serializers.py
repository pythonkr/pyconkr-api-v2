import rest_framework.serializers as serializers
from rest_framework.fields import SerializerMethodField

from sponsor.models import Patron, Sponsor, SponsorLevel


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "name",
            "desc",  # 국문/영문 모두 한 필드에 담아 제공
            "manager_name",  # 상세에만 포함되는 필드
            "manager_email",  # 상세에만 포함되는 필드
            "manager_tel",  # 상세에만 포함되는 필드
            "business_registration_number",  # 상세에만 포함되는 필드
            "business_registration_file",  # 상세에만 포함되는 필드
            "bank_book_file",  # 상세에만 포함되는 필드
            "url",
            "logo_image",
            "level",
            "id",
        ]
        read_only_fields = [
            "name",
            "level",
            "id",
        ]


class SponsorDetailSerializer(serializers.ModelSerializer):
    creator_userid = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = [
            "name",
            "desc",
            "url",
            "logo_image",
            "level",
            "id",
            "creator_userid",
        ]

    @staticmethod
    def get_creator_userid(obj: Sponsor):
        return obj.creator.username if obj.creator is not None else None


class SponsorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            "name",
            "url",
            "logo_image",
            "level",
            "id",
        ]


class SponsorRemainingAccountSerializer(serializers.ModelSerializer):
    remaining = SerializerMethodField()
    available = SerializerMethodField()

    class Meta:
        model = SponsorLevel
        fields = [
            "name",
            "price",
            "limit",
            "id",
            "available",
        ]

    @staticmethod
    def get_remaining(obj):
        return obj.current_remaining_number

    @staticmethod
    def get_available(obj: SponsorLevel):
        return True if obj.current_remaining_number > 0 else False


class PatronListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patron
        fields = [
            "name",
            "contribution_message",
            "sort_order",
        ]

    sort_order = serializers.SerializerMethodField()

    def get_sort_order(self, obj: Patron):
        self._sort_order += 1
        return self._sort_order

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._sort_order = 0
