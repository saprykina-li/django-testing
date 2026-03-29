from http import HTTPStatus

from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm
from notes.tests.base import BaseNoteTestCase
from notes.tests.common import (
    ADD_URL,
    EDIT_VIEW,
    FOREIGN_NOTE_TITLE,
    FOREIGN_SLUG,
    LIST_URL,
    NOTE_SLUG,
    DEFAULT_TEXT,
)


class TestContent(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.foreign_note = Note.objects.create(
            title=FOREIGN_NOTE_TITLE,
            text=DEFAULT_TEXT,
            slug=FOREIGN_SLUG,
            author=cls.other,
        )

    def test_note_in_object_list_on_list_page(self):
        response = self.author_client.get(LIST_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, response.context['object_list'])

    def test_list_does_not_include_other_users_notes(self):
        response = self.author_client.get(LIST_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.foreign_note, response.context['object_list'])

    def test_add_page_has_form_in_context(self):
        response = self.author_client.get(ADD_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_edit_page_has_form_in_context(self):
        edit_url = reverse(EDIT_VIEW, kwargs={'slug': NOTE_SLUG})
        response = self.author_client.get(edit_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context['form'], NoteForm)
