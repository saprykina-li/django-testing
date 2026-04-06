from http import HTTPStatus

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.base import BaseNoteTestCase
from notes.tests.constants import (
    ADD_URL,
    DEFAULT_TEXT,
    FOREIGN_NOTE_TITLE,
    FOREIGN_SLUG,
    LIST_URL,
    NOTE_EDIT_URL,
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
        response = self.author_client.get(NOTE_EDIT_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsInstance(response.context['form'], NoteForm)
