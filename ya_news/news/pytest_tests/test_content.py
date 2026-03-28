import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, news_home_bulk):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    count = object_list.count()
    assert count <= settings.NEWS_COUNT_ON_HOME_PAGE
    assert count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_home_bulk):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, news_detail_setup):
    detail_url = news_detail_setup['detail_url']
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_detail_setup):
    detail_url = news_detail_setup['detail_url']
    response = client.get(detail_url)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(client, news_detail_setup):
    author = news_detail_setup['author']
    detail_url = news_detail_setup['detail_url']
    client.force_login(author)
    response = client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
