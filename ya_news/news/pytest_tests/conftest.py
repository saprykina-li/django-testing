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


@pytest.fixture
def news_detail_setup(db):
    news = News.objects.create(title='Заголовок', text='Текст')
    detail_url = reverse('news:detail', args=(news.id,))
    author = User.objects.create(username='Автор комментариев')
    now = timezone.now()
    first = Comment.objects.create(
        news=news,
        author=author,
        text='Старый комментарий',
    )
    second = Comment.objects.create(
        news=news,
        author=author,
        text='Новый комментарий',
    )
    Comment.objects.filter(pk=first.pk).update(
        created=now - timedelta(hours=2),
    )
    Comment.objects.filter(pk=second.pk).update(
        created=now - timedelta(hours=1),
    )
    return {
        'news': news,
        'detail_url': detail_url,
        'author': author,
    }


@pytest.fixture
def news_comment_context(db):
    news = News.objects.create(title='Заголовок', text='Текст')
    user = User.objects.create(username='Мимо Крокодил')
    url = reverse('news:detail', args=(news.id,))
    return {'news': news, 'user': user, 'url': url}


@pytest.fixture
def comment_edit_scenario(db):
    news = News.objects.create(title='Заголовок', text='Текст')
    news_url = reverse('news:detail', args=(news.id,))
    author = User.objects.create(username='Автор комментария')
    reader = User.objects.create(username='Читатель')
    author_client = Client()
    author_client.force_login(author)
    reader_client = Client()
    reader_client.force_login(reader)
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return {
        'news': news,
        'url_to_comments': news_url + '#comments',
        'author': author,
        'reader': reader,
        'author_client': author_client,
        'reader_client': reader_client,
        'comment': comment,
        'edit_url': reverse('news:edit', args=(comment.id,)),
        'delete_url': reverse('news:delete', args=(comment.id,)),
    }


@pytest.fixture
def routes_news_bundle(db):
    news = News.objects.create(title='Заголовок', text='Текст')
    author = User.objects.create(username='Лев Толстой')
    reader = User.objects.create(username='Читатель простой')
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return {
        'news': news,
        'author': author,
        'reader': reader,
        'comment': comment,
    }
