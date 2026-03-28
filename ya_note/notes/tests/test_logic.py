from http import HTTPStatus

from pytils.translit import slugify

from django.urls import reverse

from notes.models import Note
from notes.tests.base import BaseNoteTestCase


class TestLogic(BaseNoteTestCase):

    def test_logged_in_user_can_create_note(self):
        self.client.force_login(self.author)
        add_url = reverse('notes:add')
        form_data = {
            'title': 'Новая заметка',
            'text': 'Описание',
            'slug': 'new-note-slug',
        }

        response = self.client.post(add_url, data=form_data)

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
        add_url = reverse('notes:add')
        form_data = {
            'title': 'Попытка',
            'text': 'Текст',
            'slug': 'anon-attempt',
        }

        response = self.client.post(add_url, data=form_data)

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next={add_url}',
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(slug='anon-attempt').exists())

    def test_empty_slug_is_slugified_from_title(self):
        self.client.force_login(self.author)
        title = 'Транслит заголовка'
        add_url = reverse('notes:add')
        form_data = {
            'title': title,
            'text': 'Текст',
            'slug': '',
        }

        response = self.client.post(add_url, data=form_data)

        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        note = Note.objects.get(title=title, author=self.author)
        self.assertEqual(note.slug, slugify(title)[:100])

    def test_author_can_edit_own_note(self):
        self.client.force_login(self.author)
        edit_url = reverse('notes:edit', kwargs={'slug': self.note.slug})
        form_data = {
            'title': 'Обновлённый заголовок',
            'text': 'Новый текст',
            'slug': self.note.slug,
        }

        response = self.client.post(edit_url, data=form_data)

        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Обновлённый заголовок')

    def test_author_can_delete_own_note(self):
        self.client.force_login(self.author)
        delete_url = reverse('notes:delete', kwargs={'slug': self.note.slug})

        response = self.client.post(delete_url)

        self.assertRedirects(
            response,
            reverse('notes:success'),
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_foreign_user_post_edit_does_not_change_note_in_db(self):
        self.client.force_login(self.other)
        edit_url = reverse('notes:edit', kwargs={'slug': self.note.slug})
        original_title = self.note.title
        original_text = self.note.text
        form_data = {
            'title': 'Попытка подмены заголовка',
            'text': 'Попытка подмены текста',
            'slug': self.note.slug,
        }

        self.client.post(edit_url, data=form_data)

        self.note.refresh_from_db()
        self.assertEqual(self.note.title, original_title)
        self.assertEqual(self.note.text, original_text)

    def test_foreign_user_post_delete_does_not_remove_note_from_db(self):
        self.client.force_login(self.other)
        delete_url = reverse('notes:delete', kwargs={'slug': self.note.slug})
        note_pk = self.note.pk
        expected_title = self.note.title
        expected_author = self.author

        self.client.post(delete_url)

        self.assertTrue(Note.objects.filter(pk=note_pk).exists())
        note = Note.objects.get(pk=note_pk)
        self.assertEqual(note.title, expected_title)
        self.assertEqual(note.author, expected_author)


class TestDuplicateSlug(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Note.objects.create(
            title='Первая',
            text='Текст',
            slug='duplicate-slug',
            author=cls.author,
        )

    def test_cannot_create_note_with_existing_slug(self):
        self.client.force_login(self.author)
        add_url = reverse('notes:add')
        form_data = {
            'title': 'Вторая',
            'text': 'Другой текст',
            'slug': 'duplicate-slug',
        }

        response = self.client.post(add_url, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Note.objects.filter(slug='duplicate-slug').count(), 1)
