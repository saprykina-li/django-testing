from pytils.translit import slugify

from django.urls import reverse

from notes.models import Note
from notes.tests.base import BaseNoteTestCase


class TestLogic(BaseNoteTestCase):
    """Логика создания, slug и права на изменение заметок."""

    def test_logged_in_user_can_create_note(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse('notes:add'),
            data={
                'title': 'Новая заметка',
                'text': 'Описание',
                'slug': 'new-note-slug',
            },
        )
        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            Note.objects.filter(
                slug='new-note-slug',
                author=self.author,
            ).exists(),
        )

    def test_anonymous_cannot_create_note(self):
        response = self.client.post(
            reverse('notes:add'),
            data={
                'title': 'Попытка',
                'text': 'Текст',
                'slug': 'anon-attempt',
            },
        )
        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next={reverse("notes:add")}',
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(slug='anon-attempt').exists())

    def test_cannot_create_two_notes_with_same_slug(self):
        self.client.force_login(self.author)
        first = self.client.post(
            reverse('notes:add'),
            data={
                'title': 'Первая',
                'text': 'Текст',
                'slug': 'duplicate-slug',
            },
        )
        self.assertRedirects(
            first,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        second = self.client.post(
            reverse('notes:add'),
            data={
                'title': 'Вторая',
                'text': 'Другой текст',
                'slug': 'duplicate-slug',
            },
        )
        self.assertEqual(second.status_code, 200)
        self.assertFalse(second.context['form'].is_valid())
        self.assertEqual(Note.objects.filter(slug='duplicate-slug').count(), 1)

    def test_empty_slug_is_slugified_from_title(self):
        self.client.force_login(self.author)
        title = 'Транслит заголовка'
        response = self.client.post(
            reverse('notes:add'),
            data={
                'title': title,
                'text': 'Текст',
                'slug': '',
            },
        )
        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        note = Note.objects.get(title=title, author=self.author)
        self.assertEqual(note.slug, slugify(title)[:100])

    def test_author_can_edit_and_delete_own_note(self):
        self.client.force_login(self.author)
        edit_url = reverse('notes:edit', kwargs={'slug': self.note.slug})
        response = self.client.post(
            edit_url,
            data={
                'title': 'Обновлённый заголовок',
                'text': 'Новый текст',
                'slug': self.note.slug,
            },
        )
        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Обновлённый заголовок')

        delete_url = reverse('notes:delete', kwargs={'slug': self.note.slug})
        response = self.client.post(delete_url)
        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_user_cannot_edit_or_delete_foreign_note(self):
        self.client.force_login(self.other)
        for name in ('notes:edit', 'notes:delete'):
            with self.subTest(name=name):
                response = self.client.get(
                    reverse(name, kwargs={'slug': self.note.slug}),
                )
                self.assertEqual(response.status_code, 404)
