from http import HTTPStatus

from notes.tests.base import BaseNoteTestCase
from notes.tests.constants import (
    ADD_URL,
    HOME_URL,
    LIST_URL,
    LOGIN_URL,
    LOGOUT_URL,
    NOTE_DELETE_URL,
    NOTE_DETAIL_URL,
    NOTE_EDIT_URL,
    SIGNUP_URL,
    SUCCESS_URL,
)


class TestRoutes(BaseNoteTestCase):

    def test_get_page_returns_expected_status(self):
        cases = (
            (self.anonymous_client, HOME_URL, HTTPStatus.OK),
            (self.author_client, LIST_URL, HTTPStatus.OK),
            (self.author_client, SUCCESS_URL, HTTPStatus.OK),
            (self.author_client, ADD_URL, HTTPStatus.OK),
            (self.author_client, NOTE_DETAIL_URL, HTTPStatus.OK),
            (self.author_client, NOTE_EDIT_URL, HTTPStatus.OK),
            (self.author_client, NOTE_DELETE_URL, HTTPStatus.OK),
            (self.other_client, NOTE_DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.other_client, NOTE_EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.other_client, NOTE_DELETE_URL, HTTPStatus.NOT_FOUND),
        )
        for client, url, expected_status in cases:
            with self.subTest(url=url, expected_status=expected_status):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        for url in (
            LIST_URL,
            SUCCESS_URL,
            ADD_URL,
            NOTE_DETAIL_URL,
            NOTE_EDIT_URL,
            NOTE_DELETE_URL,
        ):
            with self.subTest(url=url):
                expected_redirect = f'{LOGIN_URL}?next={url}'
                response = self.anonymous_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                self.assertRedirects(
                    response,
                    expected_redirect,
                    fetch_redirect_response=False,
                )

    def test_auth_pages_return_ok_on_get(self):
        cases = (
            (self.anonymous_client, LOGIN_URL),
            (self.anonymous_client, SIGNUP_URL),
            (self.author_client, LOGIN_URL),
            (self.author_client, SIGNUP_URL),
        )
        for client, url in cases:
            logged_in = client is self.author_client
            with self.subTest(url=url, logged_in=logged_in):
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_returns_ok_on_post(self):
        for client in (self.anonymous_client, self.author_client):
            logged_in = client is self.author_client
            with self.subTest(logged_in=logged_in):
                response = client.post(LOGOUT_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)
