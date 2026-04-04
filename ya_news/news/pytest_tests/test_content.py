import pytest
from django.conf import settings

from news.forms import CommentForm
from news.pytest_tests.common import HOME_URL

pytestmark = pytest.mark.django_db


def test_news_count(anonymous_client, news_home_bulk):
    expected_count = settings.NEWS_COUNT_ON_HOME_PAGE
    url = HOME_URL

    response = anonymous_client.get(url)

    object_list = response.context['object_list']
    assert len(news_home_bulk) == expected_count + 1
    assert object_list.count() == expected_count


def test_news_order(anonymous_client, news_home_bulk):
    expected_first_date = news_home_bulk[0].date
    url = HOME_URL

    response = anonymous_client.get(url)

    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)
    assert object_list[0].date == expected_first_date


def test_comments_order(
    anonymous_client,
    news_detail_url,
    comments_chronological_pair,
):
    expected_comments = comments_chronological_pair
    url = news_detail_url

    response = anonymous_client.get(url)

    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert [comment.pk for comment in all_comments] == [
        expected_comment.pk for expected_comment in expected_comments
    ]
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(anonymous_client, news_detail_url):
    url = news_detail_url

    response = anonymous_client.get(url)

    assert 'form' not in response.context


def test_authorized_client_has_form(
    user_author_on_detail_page_client,
    news_detail_url,
):
    url = news_detail_url

    response = user_author_on_detail_page_client.get(url)

    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
