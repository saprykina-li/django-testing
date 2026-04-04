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
            (
                'anonymous',
                'home',
                self.anonymous_client,
                HOME_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'list',
                self.author_client,
                LIST_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'success',
                self.author_client,
                SUCCESS_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'add',
                self.author_client,
                ADD_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'detail',
                self.author_client,
                NOTE_DETAIL_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'edit',
                self.author_client,
                NOTE_EDIT_URL,
                HTTPStatus.OK,
            ),
            (
                'author',
                'delete',
                self.author_client,
                NOTE_DELETE_URL,
                HTTPStatus.OK,
            ),
            (
                'other',
                'detail',
                self.other_client,
                NOTE_DETAIL_URL,
                HTTPStatus.NOT_FOUND,
            ),
            (
                'other',
                'edit',
                self.other_client,
                NOTE_EDIT_URL,
                HTTPStatus.NOT_FOUND,
            ),
            (
                'other',
                'delete',
                self.other_client,
                NOTE_DELETE_URL,
                HTTPStatus.NOT_FOUND,
            ),
        )
        for user_label, page, client, url, expected_status in cases:
            with self.subTest(
                user=user_label,
                page=page,
                expected_status=expected_status,
            ):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        protected_urls = (
            ('list', LIST_URL),
            ('success', SUCCESS_URL),
            ('add', ADD_URL),
            ('detail', NOTE_DETAIL_URL),
            ('edit', NOTE_EDIT_URL),
            ('delete', NOTE_DELETE_URL),
        )
        for page, url in protected_urls:
            with self.subTest(page=page):
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
            ('anonymous', 'login', self.anonymous_client, LOGIN_URL),
            ('anonymous', 'signup', self.anonymous_client, SIGNUP_URL),
            ('author', 'login', self.author_client, LOGIN_URL),
            ('author', 'signup', self.author_client, SIGNUP_URL),
        )
        for user_label, page, client, url in cases:
            with self.subTest(user=user_label, page=page, method='GET'):
                response = client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_returns_ok_on_post(self):
        cases = (
            ('anonymous', self.anonymous_client),
            ('author', self.author_client),
        )
        for user_label, client in cases:
            with self.subTest(user=user_label, method='POST'):
                response = client.post(LOGOUT_URL)
                self.assertEqual(response.status_code, HTTPStatus.OK)
