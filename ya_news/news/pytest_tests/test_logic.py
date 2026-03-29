from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'
DETAIL_URL_NAME = 'news:detail'
EDIT_URL_NAME = 'news:edit'
DELETE_URL_NAME = 'news:delete'


def test_anonymous_user_cant_create_comment(
    anonymous_client,
    news_detail_url,
):
    # Arrange
    form_data = {'text': COMMENT_TEXT}

    # Act
    anonymous_client.post(news_detail_url, data=form_data)

    # Assert
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    news_default,
    news_detail_url,
    mimo_client,
    user_mimo_krokodil,
):
    # Arrange
    form_data = {'text': COMMENT_TEXT}

    # Act
    response = mimo_client.post(news_detail_url, data=form_data)

    # Assert
    assertRedirects(
        response,
        f'{news_detail_url}#comments',
        fetch_redirect_response=False,
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news_default
    assert comment.author == user_mimo_krokodil


def test_user_cant_use_bad_words(
    news_detail_url,
    mimo_client,
):
    # Arrange
    bad_words_data = {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст',
    }

    # Act
    response = mimo_client.post(news_detail_url, data=bad_words_data)

    # Assert
    assertFormError(response.context['form'], 'text', WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    news_default,
    comment_for_edit_flow,
    comment_author_client,
):
    # Arrange
    delete_url = reverse(DELETE_URL_NAME, args=(comment_for_edit_flow.id,))
    url_to_comments = (
        reverse(DETAIL_URL_NAME, args=(news_default.id,)) + '#comments'
    )
    # Act
    response = comment_author_client.delete(delete_url)

    # Assert
    assertRedirects(
        response,
        url_to_comments,
        fetch_redirect_response=False,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    comment_for_edit_flow,
    user_comment_author,
    chitatel_client,
):
    # Arrange
    delete_url = reverse(DELETE_URL_NAME, args=(comment_for_edit_flow.id,))
    # Act
    chitatel_client.delete(delete_url)

    # Assert
    assert Comment.objects.count() == 1
    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == COMMENT_TEXT
    assert comment_for_edit_flow.author == user_comment_author


def test_author_can_edit_comment(
    news_default,
    comment_for_edit_flow,
    comment_author_client,
):
    # Arrange
    edit_url = reverse(EDIT_URL_NAME, args=(comment_for_edit_flow.id,))
    url_to_comments = (
        reverse(DETAIL_URL_NAME, args=(news_default.id,)) + '#comments'
    )
    form_data = {'text': NEW_COMMENT_TEXT}

    # Act
    response = comment_author_client.post(edit_url, data=form_data)

    # Assert
    assertRedirects(
        response,
        url_to_comments,
        fetch_redirect_response=False,
    )
    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
    comment_for_edit_flow,
    user_comment_author,
    chitatel_client,
):
    # Arrange
    edit_url = reverse(EDIT_URL_NAME, args=(comment_for_edit_flow.id,))
    form_data = {'text': NEW_COMMENT_TEXT}

    # Act
    chitatel_client.post(edit_url, data=form_data)

    # Assert
    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == COMMENT_TEXT
    assert comment_for_edit_flow.author == user_comment_author
