import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from sponsor.models import Patron, SponsorLevel

pytestmark = pytest.mark.django_db

UserModel = get_user_model()


client = APIClient()


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


@pytest.mark.django_db
class TestPatron:
    pytestmark = pytest.mark.django_db

    def test_patron_list_api(self):
        assert Patron.objects.count() == 0
        response = client.get("/sponsors/patron/list/", format="json")
        assert response.status_code == 200
        assert len(response.data) == 0

        Patron.objects.create(
            name="Python Lover 1",
            contribution_message="I love Python",
            total_contribution=1000000,
            contribution_datetime="2023-07-27 00:00:00+09:00",
        )
        assert Patron.objects.count() == 1
        response = client.get("/sponsors/patron/list/", format="json")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Python Lover 1"
        # check sort order
        assert response.data[0]["sort_order"] == 1

        # add second patron
        Patron.objects.create(
            name="Python Lover 2",
            contribution_message="I love Python too",
            total_contribution=1000001,
            contribution_datetime="2023-07-27 00:00:00+09:00",
        )
        assert Patron.objects.count() == 2
        response = client.get("/sponsors/patron/list/", format="json")
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["name"] == "Python Lover 2"
        # check sort order
        assert response.data[0]["sort_order"] == 1
        assert response.data[1]["name"] == "Python Lover 1"
        assert response.data[1]["sort_order"] == 2

        # add third patron
        # check contribution_datetime is earlier than Python Lover 2
        Patron.objects.create(
            name="Python Lover 3",
            contribution_message="I love Python most",
            total_contribution=1000001,
            # earlier contribution then Python Lover 2
            contribution_datetime="2023-07-26 00:00:00+09:00",
        )
        assert Patron.objects.count() == 3
        response = client.get("/sponsors/patron/list/", format="json")
        assert response.status_code == 200
        assert len(response.data) == 3
        assert response.data[0]["name"] == "Python Lover 3"
        # check sort order
        assert response.data[0]["sort_order"] == 1
        assert response.data[1]["name"] == "Python Lover 2"
        assert response.data[1]["sort_order"] == 2

    @pytest.skip("TODO: implement")
    def test_patron_message_html_sanitizer(self):
        assert Patron.objects.count() == 0
        # check patron save will sanitize html field
        # allow only <a> tag
        # allow emoji
        pass
