from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db

HOME_URL_NAME = 'news:home'
DETAIL_URL_NAME = 'news:detail'
LOGIN_URL = reverse('users:login')
SIGNUP_URL = reverse('users:signup')
LOGOUT_URL = reverse('users:logout')
EDIT_URL_NAME = 'news:edit'
DELETE_URL_NAME = 'news:delete'


def test_home_available_to_anonymous(client):
    # Arrange
    url = reverse(HOME_URL_NAME)

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == HTTPStatus.OK


def test_detail_available_to_anonymous(client, news_default):
    # Arrange
    url = reverse(DETAIL_URL_NAME, args=(news_default.id,))

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('url', (LOGIN_URL, SIGNUP_URL, LOGOUT_URL))
def test_auth_pages_available_to_anonymous(client, url):
    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ('user', 'viewname', 'expected'),
    (
        (lazy_fixture('user_lev_tolstoy'), EDIT_URL_NAME, HTTPStatus.OK),
        (lazy_fixture('user_lev_tolstoy'), DELETE_URL_NAME, HTTPStatus.OK),
        (
            lazy_fixture('user_chitatel_prostoy'),
            EDIT_URL_NAME,
            HTTPStatus.NOT_FOUND,
        ),
        (
            lazy_fixture('user_chitatel_prostoy'),
            DELETE_URL_NAME,
            HTTPStatus.NOT_FOUND,
        ),
    ),
)
def test_availability_for_comment_edit_and_delete(
    comment_by_lev,
    user,
    viewname,
    expected,
):
    # Arrange
    auth_client = Client()
    auth_client.force_login(user)
    url = reverse(viewname, args=(comment_by_lev.id,))

    # Act
    response = auth_client.get(url)

    # Assert
    assert response.status_code == expected


@pytest.mark.parametrize('viewname', (EDIT_URL_NAME, DELETE_URL_NAME))
def test_redirect_for_anonymous_client(client, comment_by_lev, viewname):
    # Arrange
    url = reverse(viewname, args=(comment_by_lev.id,))
    redirect_url = f'{LOGIN_URL}?next={url}'

    # Act
    response = client.get(url)

    # Assert
    assertRedirects(response, redirect_url, fetch_redirect_response=False)
