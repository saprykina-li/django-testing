from django.urls import reverse

from notes.tests.base import BaseNoteTestCase


class TestRoutes(BaseNoteTestCase):
    """Доступность страниц в зависимости от пользователя."""

    def test_home_page_available_for_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, 200)

    def test_list_success_add_available_for_authenticated(self):
        self.client.force_login(self.author)
        for name in ('notes:list', 'notes:success', 'notes:add'):
            with self.subTest(url=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_detail_edit_delete_only_for_author(self):
        self.client.force_login(self.other)
        for name in ('notes:detail', 'notes:edit', 'notes:delete'):
            with self.subTest(url=name):
                response = self.client.get(
                    reverse(name, kwargs={'slug': self.note.slug}),
                )
                self.assertEqual(response.status_code, 404)

    def test_anonymous_redirected_to_login_for_protected_pages(self):
        urls = [
            reverse('notes:list'),
            reverse('notes:success'),
            reverse('notes:add'),
            reverse('notes:detail', kwargs={'slug': self.note.slug}),
            reverse('notes:edit', kwargs={'slug': self.note.slug}),
            reverse('notes:delete', kwargs={'slug': self.note.slug}),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'{reverse("users:login")}?next={url}',
                    fetch_redirect_response=False,
                )

    def test_auth_pages_available_for_anonymous(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)

    def test_auth_pages_available_for_authenticated(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 200)
