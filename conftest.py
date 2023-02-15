import pytest


# TODO
# https://djangostars.com/blog/django-pytest-testing/#header17
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()
