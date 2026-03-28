from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from notes.tests.base import BaseNoteTestCase


class TestContent(BaseNoteTestCase):
    """Контекст шаблонов и данные в object_list."""

    def test_note_in_object_list_on_list_page(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note, response.context['object_list'])

    def test_list_does_not_include_other_users_notes(self):
        foreign = Note.objects.create(
            title='Чужая заметка',
            text='Текст',
            slug='foreign-slug',
            author=self.other,
        )
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note, response.context['object_list'])
        self.assertNotIn(foreign, response.context['object_list'])

    def test_create_and_edit_pages_have_forms_in_context(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], NoteForm)

        response = self.client.get(
            reverse('notes:edit', kwargs={'slug': self.note.slug}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], NoteForm)
