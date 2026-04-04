from http import HTTPStatus

import pytest
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects

from news.pytest_tests.common import (
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
)

pytestmark = pytest.mark.django_db


def test_home_available_to_anonymous(anonymous_client):
    url = HOME_URL

    response = anonymous_client.get(url)

    assert response.status_code == HTTPStatus.OK


def test_detail_available_to_anonymous(anonymous_client, news_detail_url):
    url = news_detail_url

    response = anonymous_client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url', (LOGIN_URL, SIGNUP_URL, LOGOUT_URL))
def test_auth_pages_available_to_anonymous(anonymous_client, url):
    response = anonymous_client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ('auth_client', 'url', 'expected'),
    (
        (
            lazy_fixture('user_comment_owner_client'),
            lazy_fixture('comment_by_owner_edit_url'),
            HTTPStatus.OK,
        ),
        (
            lazy_fixture('user_comment_owner_client'),
            lazy_fixture('comment_by_owner_delete_url'),
            HTTPStatus.OK,
        ),
        (
            lazy_fixture('user_other_reader_client'),
            lazy_fixture('comment_by_owner_edit_url'),
            HTTPStatus.NOT_FOUND,
        ),
        (
            lazy_fixture('user_other_reader_client'),
            lazy_fixture('comment_by_owner_delete_url'),
            HTTPStatus.NOT_FOUND,
        ),
    ),
)
def test_availability_for_comment_edit_and_delete(
    auth_client,
    url,
    expected,
):
    response = auth_client.get(url)

    assert response.status_code == expected


@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('comment_by_owner_edit_url'),
        lazy_fixture('comment_by_owner_delete_url'),
    ),
)
def test_redirect_for_anonymous_client(anonymous_client, url):
    redirect_url = f'{LOGIN_URL}?next={url}'

    response = anonymous_client.get(url)

    assertRedirects(response, redirect_url, fetch_redirect_response=False)
