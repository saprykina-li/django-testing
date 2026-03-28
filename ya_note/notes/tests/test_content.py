from http import HTTPStatus

from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from notes.tests.base import BaseNoteTestCase


class TestContent(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.foreign_note = Note.objects.create(
            title='Чужая заметка',
            text='Текст',
            slug='foreign-slug',
            author=cls.other,
        )

    def test_note_in_object_list_on_list_page(self):
        self.client.force_login(self.author)
        list_url = reverse('notes:list')

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, response.context['object_list'])

    def test_list_does_not_include_other_users_notes(self):
        self.client.force_login(self.author)
        list_url = reverse('notes:list')

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.foreign_note, response.context['object_list'])

    def test_add_page_has_form_in_context(self):
        self.client.force_login(self.author)
        add_url = reverse('notes:add')

        response = self.client.get(add_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_page_has_form_in_context(self):
        self.client.force_login(self.author)
        edit_url = reverse('notes:edit', kwargs={'slug': self.note.slug})

        response = self.client.get(edit_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context['form'], NoteForm)
