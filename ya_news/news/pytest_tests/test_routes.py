from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

from news.pytest_tests.common import (
    HOME_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
)

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url',
    (
        HOME_URL,
        LOGIN_URL,
        SIGNUP_URL,
        LOGOUT_URL,
        lazy_fixture('news_detail_url'),
    ),
)
def test_public_pages_available_to_anonymous(anonymous_client, url):
    response = anonymous_client.get(url)

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ('client_fixture_name', 'url', 'expected_status'),
    (
        (
            'user_comment_owner_client',
            lazy_fixture('comment_by_owner_edit_url'),
            HTTPStatus.OK,
        ),
        (
            'user_comment_owner_client',
            lazy_fixture('comment_by_owner_delete_url'),
            HTTPStatus.OK,
        ),
        (
            'user_other_reader_client',
            lazy_fixture('comment_by_owner_edit_url'),
            HTTPStatus.NOT_FOUND,
        ),
        (
            'user_other_reader_client',
            lazy_fixture('comment_by_owner_delete_url'),
            HTTPStatus.NOT_FOUND,
        ),
    ),
)
def test_comment_operations_permissions(
    client_fixture_name,
    url,
    expected_status,
    request,
):
    client = request.getfixturevalue(client_fixture_name)

    response = client.get(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        lazy_fixture('comment_by_owner_edit_url'),
        lazy_fixture('comment_by_owner_delete_url'),
    ),
)
def test_redirect_anonymous_to_login(anonymous_client, url):
    redirect_url = f'{LOGIN_URL}?next={url}'

    response = anonymous_client.get(url)

    assertRedirects(response, redirect_url, fetch_redirect_response=False)
