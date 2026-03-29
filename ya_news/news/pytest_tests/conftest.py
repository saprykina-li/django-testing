from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

User = get_user_model()


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
    return reverse('news:detail', args=(news_default.id,))


@pytest.fixture
def user_author_on_detail_page(db):
    return User.objects.create(username='Автор комментариев')


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
def user_mimo_krokodil(db):
    return User.objects.create(username='Мимо Крокодил')


@pytest.fixture
def user_lev_tolstoy(db):
    return User.objects.create(username='Лев Толстой')


@pytest.fixture
def user_chitatel_prostoy(db):
    return User.objects.create(username='Читатель простой')


@pytest.fixture
def user_comment_author(db):
    return User.objects.create(username='Автор комментария')


@pytest.fixture
def user_chitatel(db):
    return User.objects.create(username='Читатель')


@pytest.fixture
def anonymous_client():
    return Client()


@pytest.fixture
def mimo_client(user_mimo_krokodil):
    client = Client()
    client.force_login(user_mimo_krokodil)
    return client


@pytest.fixture
def comment_author_client(user_comment_author):
    client = Client()
    client.force_login(user_comment_author)
    return client


@pytest.fixture
def chitatel_client(user_chitatel):
    client = Client()
    client.force_login(user_chitatel)
    return client


@pytest.fixture
def comment_by_lev(db, news_default, user_lev_tolstoy):
    return Comment.objects.create(
        news=news_default,
        author=user_lev_tolstoy,
        text='Текст комментария',
    )


@pytest.fixture
def comment_for_edit_flow(db, news_default, user_comment_author):
    return Comment.objects.create(
        news=news_default,
        author=user_comment_author,
        text='Текст комментария',
    )
