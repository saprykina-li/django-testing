from http import HTTPStatus

import pytest
from django.test import Client
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news_comment_context):
    url = news_comment_context['url']
    form_data = {'text': COMMENT_TEXT}
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(news_comment_context):
    news = news_comment_context['news']
    user = news_comment_context['user']
    url = news_comment_context['url']
    auth_client = Client()
    auth_client.force_login(user)
    form_data = {'text': COMMENT_TEXT}
    response = auth_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments', fetch_redirect_response=False)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_TEXT
    assert comment.news == news
    assert comment.author == user


@pytest.mark.django_db
def test_user_cant_use_bad_words(news_comment_context):
    user = news_comment_context['user']
    url = news_comment_context['url']
    auth_client = Client()
    auth_client.force_login(user)
    bad_words_data = {
        'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст',
    }
    response = auth_client.post(url, data=bad_words_data)
    assertFormError(response.context['form'], 'text', WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_author_can_delete_comment(comment_edit_scenario):
    author_client = comment_edit_scenario['author_client']
    delete_url = comment_edit_scenario['delete_url']
    url_to_comments = comment_edit_scenario['url_to_comments']
    response = author_client.delete(delete_url)
    assertRedirects(
        response,
        url_to_comments,
        fetch_redirect_response=False,
    )
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(comment_edit_scenario):
    reader_client = comment_edit_scenario['reader_client']
    delete_url = comment_edit_scenario['delete_url']
    comment = comment_edit_scenario['comment']
    author = comment_edit_scenario['author']
    reader_client.delete(delete_url)
    assert Comment.objects.count() == 1
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
    assert comment.author == author


@pytest.mark.django_db
def test_author_can_edit_comment(comment_edit_scenario):
    author_client = comment_edit_scenario['author_client']
    edit_url = comment_edit_scenario['edit_url']
    url_to_comments = comment_edit_scenario['url_to_comments']
    comment = comment_edit_scenario['comment']
    form_data = {'text': NEW_COMMENT_TEXT}
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(
        response,
        url_to_comments,
        fetch_redirect_response=False,
    )
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(comment_edit_scenario):
    reader_client = comment_edit_scenario['reader_client']
    edit_url = comment_edit_scenario['edit_url']
    comment = comment_edit_scenario['comment']
    author = comment_edit_scenario['author']
    form_data = {'text': NEW_COMMENT_TEXT}
    reader_client.post(edit_url, data=form_data)
    comment.refresh_from_db()
    assert comment.text == COMMENT_TEXT
    assert comment.author == author
