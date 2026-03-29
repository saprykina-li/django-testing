from http import HTTPStatus

from django.urls import reverse

from notes.tests.base import BaseNoteTestCase
from notes.tests.common import (
    ADD_VIEW,
    DELETE_VIEW,
    DETAIL_VIEW,
    EDIT_VIEW,
    HOME_VIEW,
    LIST_VIEW,
    LOGIN_VIEW,
    LOGOUT_VIEW,
    NOTE_SLUG,
    SIGNUP_VIEW,
    SUCCESS_VIEW,
)


class TestRoutes(BaseNoteTestCase):

    def test_home_page_is_ok_for_anonymous_user(self):
        url = reverse(HOME_VIEW)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_list_is_ok_for_author(self):
        url = reverse(LIST_VIEW)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_success_page_is_ok_for_author(self):
        url = reverse(SUCCESS_VIEW)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_page_is_ok_for_author(self):
        url = reverse(ADD_VIEW)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page_is_ok_for_author(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DETAIL_VIEW, kwargs=note_slug_kwargs)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_page_is_ok_for_author(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(EDIT_VIEW, kwargs=note_slug_kwargs)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_page_is_ok_for_author(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DELETE_VIEW, kwargs=note_slug_kwargs)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_returns_not_found_for_other_user(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DETAIL_VIEW, kwargs=note_slug_kwargs)
        response = self.other_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_edit_returns_not_found_for_other_user(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(EDIT_VIEW, kwargs=note_slug_kwargs)
        response = self.other_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_returns_not_found_for_other_user(self):
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DELETE_VIEW, kwargs=note_slug_kwargs)
        response = self.other_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_anonymous_redirected_to_login_for_list(self):
        login_url = reverse(LOGIN_VIEW)
        url = reverse(LIST_VIEW)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_anonymous_redirected_to_login_for_success(self):
        login_url = reverse(LOGIN_VIEW)
        url = reverse(SUCCESS_VIEW)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_anonymous_redirected_to_login_for_add(self):
        login_url = reverse(LOGIN_VIEW)
        url = reverse(ADD_VIEW)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_anonymous_redirected_to_login_for_detail(self):
        login_url = reverse(LOGIN_VIEW)
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DETAIL_VIEW, kwargs=note_slug_kwargs)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_anonymous_redirected_to_login_for_edit(self):
        login_url = reverse(LOGIN_VIEW)
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(EDIT_VIEW, kwargs=note_slug_kwargs)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_anonymous_redirected_to_login_for_delete(self):
        login_url = reverse(LOGIN_VIEW)
        note_slug_kwargs = {'slug': NOTE_SLUG}
        url = reverse(DELETE_VIEW, kwargs=note_slug_kwargs)
        expected_redirect = f'{login_url}?next={url}'
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            expected_redirect,
            fetch_redirect_response=False,
        )

    def test_login_page_ok_for_anonymous(self):
        url = reverse(LOGIN_VIEW)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_signup_page_ok_for_anonymous(self):
        url = reverse(SIGNUP_VIEW)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_page_ok_for_anonymous_post(self):
        url = reverse(LOGOUT_VIEW)
        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_page_ok_for_author(self):
        url = reverse(LOGIN_VIEW)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_signup_page_ok_for_author(self):
        url = reverse(SIGNUP_VIEW)
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_page_ok_for_author_post(self):
        url = reverse(LOGOUT_VIEW)
        response = self.author_client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
