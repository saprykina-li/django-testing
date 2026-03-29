import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

pytestmark = pytest.mark.django_db

HOME_URL = reverse('news:home')
DETAIL_URL_NAME = 'news:detail'


def test_news_count(client, news_home_bulk):
    # Arrange
    expected_count = settings.NEWS_COUNT_ON_HOME_PAGE

    # Act
    response = client.get(HOME_URL)

    # Assert
    object_list = response.context['object_list']
    assert len(news_home_bulk) == expected_count + 1
    assert object_list.count() == expected_count


def test_news_order(client, news_home_bulk):
    # Arrange
    expected_first_date = news_home_bulk[0].date

    # Act
    response = client.get(HOME_URL)

    # Assert
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)
    assert object_list[0].date == expected_first_date


def test_comments_order(
    client,
    news_detail_url,
    comments_chronological_pair,
):
    # Arrange
    expected_comments = comments_chronological_pair

    # Act
    response = client.get(news_detail_url)

    # Assert
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert [c.pk for c in all_comments] == [c.pk for c in expected_comments]
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, news_detail_url):
    # Act
    response = client.get(news_detail_url)

    # Assert
    assert 'form' not in response.context


def test_authorized_client_has_form(
    client,
    news_detail_url,
    user_author_on_detail_page,
):
    # Arrange
    client.force_login(user_author_on_detail_page)

    # Act
    response = client.get(news_detail_url)

    # Assert
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
