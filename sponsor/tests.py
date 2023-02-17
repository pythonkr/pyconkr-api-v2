import pytest
from django.contrib.auth import get_user_model

from sponsor.models import SponsorLevel

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


@pytest.mark.django_db
class TestSponsorLevelModel:
    pytestmark = pytest.mark.django_db

    def test_sponsor_level_creation_success(self):
        assert SponsorLevel.objects.count() == 0
        SponsorLevel.objects.create(
            name="test",
            desc="test desc",
            visible=True,
            limit=1,
        )
        assert SponsorLevel.objects.count() != 0


# Create your tests here.
