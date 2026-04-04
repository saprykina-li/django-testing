from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

from news.pytest_tests.common import (
    NEWS_COMMENT_DELETE_URL_NAME,
    NEWS_COMMENT_EDIT_URL_NAME,
    NEWS_DETAIL_URL_NAME,
)

User = get_user_model()


def _comment_delete_url(comment):
    return reverse(
        NEWS_COMMENT_DELETE_URL_NAME,
        args=(comment.pk,),
    )


def _comment_edit_url(comment):
    return reverse(
        NEWS_COMMENT_EDIT_URL_NAME,
        args=(comment.pk,),
    )


@pytest.fixture
def news_home_bulk(db):
    today = timezone.localdate()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def news_default(db):
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def news_detail_url(news_default):
    return reverse(NEWS_DETAIL_URL_NAME, args=(news_default.id,))


@pytest.fixture
def news_detail_comments_url(news_default):
    detail_url = reverse(
        NEWS_DETAIL_URL_NAME,
        args=(news_default.id,),
    )
    return f'{detail_url}#comments'


@pytest.fixture
def comment_edit_url(comment_for_edit_flow):
    return _comment_edit_url(comment_for_edit_flow)


@pytest.fixture
def comment_delete_url(comment_for_edit_flow):
    return _comment_delete_url(comment_for_edit_flow)


@pytest.fixture
def comment_by_owner_edit_url(comment_by_owner):
    return _comment_edit_url(comment_by_owner)


@pytest.fixture
def comment_by_owner_delete_url(comment_by_owner):
    return _comment_delete_url(comment_by_owner)


@pytest.fixture
def user_author_on_detail_page(db):
    return User.objects.create(username='Автор комментариев')


@pytest.fixture
def user_author_on_detail_page_client(user_author_on_detail_page):
    client = Client()
    client.force_login(user_author_on_detail_page)
    return client


@pytest.fixture
def comments_chronological_pair(db, news_default, user_author_on_detail_page):
    now = timezone.now()
    old_comment = Comment.objects.create(
        news=news_default,
        author=user_author_on_detail_page,
        text='Старый комментарий',
    )
    new_comment = Comment.objects.create(
        news=news_default,
        author=user_author_on_detail_page,
        text='Новый комментарий',
    )
    Comment.objects.filter(pk=old_comment.pk).update(
        created=now - timedelta(hours=2),
    )
    Comment.objects.filter(pk=new_comment.pk).update(
        created=now - timedelta(hours=1),
    )
    old_comment.refresh_from_db()
    new_comment.refresh_from_db()
    return [old_comment, new_comment]


@pytest.fixture
def user_comment_creator(db):
    return User.objects.create(username='Comment Creator')


@pytest.fixture
def user_comment_owner(db):
    return User.objects.create(username='Comment Owner')


@pytest.fixture
def user_other_reader(db):
    return User.objects.create(username='Other Reader')


@pytest.fixture
def user_comment_author(db):
    return User.objects.create(username='Comment Author')


@pytest.fixture
def user_reader(db):
    return User.objects.create(username='Reader')


@pytest.fixture
def anonymous_client():
    return Client()


@pytest.fixture
def comment_creator_client(user_comment_creator):
    client = Client()
    client.force_login(user_comment_creator)
    return client


@pytest.fixture
def comment_author_client(user_comment_author):
    client = Client()
    client.force_login(user_comment_author)
    return client


@pytest.fixture
def reader_client(user_reader):
    client = Client()
    client.force_login(user_reader)
    return client


@pytest.fixture
def user_comment_owner_client(user_comment_owner):
    client = Client()
    client.force_login(user_comment_owner)
    return client


@pytest.fixture
def user_other_reader_client(user_other_reader):
    client = Client()
    client.force_login(user_other_reader)
    return client


@pytest.fixture
def comment_by_owner(db, news_default, user_comment_owner):
    return Comment.objects.create(
        news=news_default,
        author=user_comment_owner,
        text='Текст комментария',
    )


@pytest.fixture
def comment_for_edit_flow(db, news_default, user_comment_author):
    return Comment.objects.create(
        news=news_default,
        author=user_comment_author,
        text='Текст комментария',
    )
