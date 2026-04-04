from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


def test_anonymous_user_cant_create_comment(
    anonymous_client,
    news_detail_url,
):
    form_data = {'text': COMMENT_TEXT}
    url = news_detail_url

    anonymous_client.post(url, data=form_data)

    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    news_default,
    news_detail_url,
    comment_creator_client,
    user_comment_creator,
):
    form_data = {'text': COMMENT_TEXT}
    url = news_detail_url

    response = comment_creator_client.post(url, data=form_data)

    assertRedirects(
        response,
        f'{url}#comments',
        fetch_redirect_response=False,
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news_default
    assert comment.author == user_comment_creator


def test_user_cant_use_bad_words(
    news_detail_url,
    comment_creator_client,
):
    bad_words_data = {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст',
    }
    url = news_detail_url

    response = comment_creator_client.post(
        url,
        data=bad_words_data,
    )

    assertFormError(response.context['form'], 'text', WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    comment_delete_url,
    news_detail_comments_url,
    comment_author_client,
):
    response = comment_author_client.delete(comment_delete_url)

    assertRedirects(
        response,
        news_detail_comments_url,
        fetch_redirect_response=False,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    comment_delete_url,
    comment_for_edit_flow,
    user_comment_author,
    reader_client,
):
    reader_client.delete(comment_delete_url)

    assert Comment.objects.count() == 1
    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == COMMENT_TEXT
    assert comment_for_edit_flow.author == user_comment_author


def test_author_can_edit_comment(
    comment_edit_url,
    news_detail_comments_url,
    comment_for_edit_flow,
    comment_author_client,
):
    form_data = {'text': NEW_COMMENT_TEXT}

    response = comment_author_client.post(comment_edit_url, data=form_data)

    assertRedirects(
        response,
        news_detail_comments_url,
        fetch_redirect_response=False,
    )
    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(
    comment_edit_url,
    comment_for_edit_flow,
    user_comment_author,
    reader_client,
):
    form_data = {'text': NEW_COMMENT_TEXT}

    reader_client.post(comment_edit_url, data=form_data)

    comment_for_edit_flow.refresh_from_db()
    assert comment_for_edit_flow.text == COMMENT_TEXT
    assert comment_for_edit_flow.author == user_comment_author
