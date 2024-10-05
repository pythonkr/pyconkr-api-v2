import rest_framework.serializers as serializers
from rest_framework.fields import SerializerMethodField

from sponsor.models import Patron, Sponsor, SponsorLevel, SponsorBenefit, BenefitByLevel


class BenefitByLevelSerializer(serializers.ModelSerializer):
    benefit_id = serializers.PrimaryKeyRelatedField(
        queryset=SponsorBenefit.objects.all(), source="benefit"
    )
    level_id = serializers.PrimaryKeyRelatedField(
        queryset=SponsorLevel.objects.get_queryset(), source="level", write_only=True
    )

    class Meta:
        model = BenefitByLevel
        fields = ["benefit_id", "offer", "level_id"]


class SponsorBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorBenefit
        fields = ["id", "year", "name", "desc", "unit", "is_countable"]
        read_only_fields = ["id"]
        extra_kwargs = {"year": {"write_only": True}}


class SponsorBenefitWithOfferSerializer(SponsorBenefitSerializer):
    id = serializers.SlugRelatedField(slug_field="id", source="benefit", read_only=True)
    name = serializers.SlugRelatedField(
        slug_field="name", source="benefit", read_only=True
    )
    desc = serializers.SlugRelatedField(
        slug_field="desc", source="benefit", read_only=True
    )
    unit = serializers.SlugRelatedField(
        slug_field="unit", source="benefit", read_only=True
    )
    is_countable = serializers.SlugRelatedField(
        slug_field="is_countable", source="benefit", read_only=True
    )

    class Meta:
        model = BenefitByLevel
        fields = [
            "id",
            "name",
            "desc",
            "unit",
            "is_countable",
            "offer",
            "uncountable_offer",
        ]

    def get_benefit_id(self, obj):
        breakpoint()
        return

    def get_offer(self, obj):
        breakpoint()
        return obj.benefit_by_level.filter(benefit_id=obj.id)


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
        read_only_fields = ["id"]


class SponsorLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorLevel
        fields = [
            "id",
            "name",
            "desc",
            "visible",
            "price",
            "limit",
            "order",
        ]
        read_only_fields = ["id"]


class SponsorLevelWithBenefitSerializer(SponsorLevelSerializer):
    benefits = SponsorBenefitWithOfferSerializer(
        many=True, read_only=True, source="benefit_by_level"
    )

    class Meta(SponsorLevelSerializer.Meta):
        fields = SponsorLevelSerializer.Meta.fields + ["benefits"]


class SponsorSummariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["name", "desc", "url", "logo_image", "id"]


class SponsorWithLevelSerializer(serializers.ModelSerializer):
    sponsor = SponsorSummariesSerializer(
        read_only=True, many=True, source="sponsor_set"
    )

    class Meta:
        model = SponsorLevel
        fields = ["id", "name", "visible", "order", "sponsor"]


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
    level = SponsorLevelSerializer(read_only=True)

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
