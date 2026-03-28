from http import HTTPStatus

from django.test import Client
from django.urls import reverse

from notes.tests.base import BaseNoteTestCase


class TestRoutes(BaseNoteTestCase):

    def test_get_ok_for_home_and_for_authenticated_note_pages(self):
        slug_kw = {'slug': self.note.slug}
        cases = (
            (None, 'notes:home', {}),
            (self.author, 'notes:list', {}),
            (self.author, 'notes:success', {}),
            (self.author, 'notes:add', {}),
            (self.author, 'notes:detail', slug_kw),
            (self.author, 'notes:edit', slug_kw),
            (self.author, 'notes:delete', slug_kw),
        )
        for user, viewname, url_kwargs in cases:
            user_label = user.username if user is not None else 'anonymous'
            expected_status = HTTPStatus.OK
            with self.subTest(
                user=user_label,
                viewname=viewname,
                expected_status=expected_status,
            ):
                client = Client()
                if user is not None:
                    client.force_login(user)
                url = reverse(viewname, kwargs=url_kwargs)
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_other_user_get_note_pages_returns_not_found(self):
        slug_kw = {'slug': self.note.slug}
        expected_status = HTTPStatus.NOT_FOUND
        for viewname in ('notes:detail', 'notes:edit', 'notes:delete'):
            with self.subTest(
                user=self.other.username,
                viewname=viewname,
                expected_status=expected_status,
            ):
                client = Client()
                client.force_login(self.other)
                url = reverse(viewname, kwargs=slug_kw)
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        login_url = reverse('users:login')
        expected_status = HTTPStatus.FOUND
        protected = (
            ('notes:list', {}),
            ('notes:success', {}),
            ('notes:add', {}),
            ('notes:detail', {'slug': self.note.slug}),
            ('notes:edit', {'slug': self.note.slug}),
            ('notes:delete', {'slug': self.note.slug}),
        )
        for viewname, url_kwargs in protected:
            with self.subTest(
                user='anonymous',
                viewname=viewname,
                expected_status=expected_status,
            ):
                url = reverse(viewname, kwargs=url_kwargs)
                expected_redirect = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertEqual(response.status_code, expected_status)
                self.assertRedirects(
                    response,
                    expected_redirect,
                    fetch_redirect_response=False,
                )

    def test_auth_pages_return_ok_anonymous_and_authenticated(self):
        auth_routes = (
            ('GET', 'users:login'),
            ('GET', 'users:signup'),
            ('POST', 'users:logout'),
        )
        expected_status = HTTPStatus.OK
        for authenticated_user in (None, self.author):
            user_label = (
                'anonymous' if authenticated_user is None
                else authenticated_user.username
            )
            for method, viewname in auth_routes:
                with self.subTest(
                    user=user_label,
                    method=method,
                    viewname=viewname,
                    expected_status=expected_status,
                ):
                    client = Client()
                    if authenticated_user is not None:
                        client.force_login(authenticated_user)
                    url = reverse(viewname)
                    if method == 'GET':
                        response = client.get(url)
                    else:
                        response = client.post(url)
                    self.assertEqual(response.status_code, expected_status)
