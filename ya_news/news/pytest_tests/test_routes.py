from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'viewname,use_news_id',
    (
        ('news:home', False),
        ('news:detail', True),
    ),
)
def test_home_and_detail_available_to_anonymous(
    client,
    routes_news_bundle,
    viewname,
    use_news_id,
):
    news = routes_news_bundle['news']
    args = (news.id,) if use_news_id else None
    url = reverse(viewname, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'viewname',
    ('users:login', 'users:signup', 'users:logout'),
)
def test_auth_pages_available_to_anonymous(client, viewname):
    url = reverse(viewname)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('username', 'viewname', 'expected'),
    (
        ('Лев Толстой', 'news:edit', HTTPStatus.OK),
        ('Лев Толстой', 'news:delete', HTTPStatus.OK),
        ('Читатель простой', 'news:edit', HTTPStatus.NOT_FOUND),
        ('Читатель простой', 'news:delete', HTTPStatus.NOT_FOUND),
    ),
)
def test_availability_for_comment_edit_and_delete(
    routes_news_bundle,
    username,
    viewname,
    expected,
):
    author = routes_news_bundle['author']
    reader = routes_news_bundle['reader']
    comment = routes_news_bundle['comment']
    user = author if username == author.username else reader
    client = Client()
    client.force_login(user)
    url = reverse(viewname, args=(comment.id,))
    response = client.get(url)
    assert response.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize('viewname', ('news:edit', 'news:delete'))
def test_redirect_for_anonymous_client(client, routes_news_bundle, viewname):
    login_url = reverse('users:login')
    comment = routes_news_bundle['comment']
    url = reverse(viewname, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url, fetch_redirect_response=False)
