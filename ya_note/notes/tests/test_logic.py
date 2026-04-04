from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.tests.base import BaseNoteTestCase
from notes.tests.constants import (
    ADD_URL,
    ANON_ATTEMPT_SLUG,
    ANON_TITLE,
    DEFAULT_TEXT,
    DUPLICATE_FIRST_TITLE,
    DUPLICATE_SECOND_TEXT,
    DUPLICATE_SECOND_TITLE,
    DUPLICATE_SLUG,
    EDITED_TEXT,
    EDITED_TITLE,
    FOREIGN_EDIT_TEXT,
    FOREIGN_EDIT_TITLE,
    LOGIN_URL,
    NEW_NOTE_SLUG,
    NEW_TEXT,
    NEW_TITLE,
    NOTE_DELETE_URL,
    NOTE_EDIT_URL,
    NOTE_SLUG,
    SLUGIFIED_TITLE,
    SUCCESS_URL,
)


class TestLogic(BaseNoteTestCase):

    def test_logged_in_user_can_create_note(self):
        form_data = {
            'title': NEW_TITLE,
            'text': NEW_TEXT,
            'slug': NEW_NOTE_SLUG,
        }

        response = self.author_client.post(ADD_URL, data=form_data)

        self.assertRedirects(
            response,
            SUCCESS_URL,
            fetch_redirect_response=False,
        )
        self.assertTrue(
            Note.objects.filter(
                slug=NEW_NOTE_SLUG,
                author=self.author,
            ).exists(),
        )

    def test_anonymous_cannot_create_note(self):
        form_data = {
            'title': ANON_TITLE,
            'text': DEFAULT_TEXT,
            'slug': ANON_ATTEMPT_SLUG,
        }

        response = self.anonymous_client.post(ADD_URL, data=form_data)

        self.assertRedirects(
            response,
            f'{LOGIN_URL}?next={ADD_URL}',
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(slug=ANON_ATTEMPT_SLUG).exists())

    def test_empty_slug_is_slugified_from_title(self):
        title = SLUGIFIED_TITLE
        form_data = {
            'title': title,
            'text': DEFAULT_TEXT,
            'slug': '',
        }

        response = self.author_client.post(ADD_URL, data=form_data)

        self.assertRedirects(
            response,
            SUCCESS_URL,
            fetch_redirect_response=False,
        )
        note = Note.objects.get(title=title, author=self.author)
        self.assertEqual(note.slug, slugify(title)[:100])

    def test_author_can_edit_own_note(self):
        form_data = {
            'title': EDITED_TITLE,
            'text': EDITED_TEXT,
            'slug': NOTE_SLUG,
        }

        response = self.author_client.post(NOTE_EDIT_URL, data=form_data)

        self.assertRedirects(
            response,
            SUCCESS_URL,
            fetch_redirect_response=False,
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, EDITED_TITLE)

    def test_author_can_delete_own_note(self):
        response = self.author_client.post(NOTE_DELETE_URL)

        self.assertRedirects(
            response,
            SUCCESS_URL,
            fetch_redirect_response=False,
        )
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_foreign_user_post_edit_does_not_change_note_in_db(self):
        original_title = self.note.title
        original_text = self.note.text
        form_data = {
            'title': FOREIGN_EDIT_TITLE,
            'text': FOREIGN_EDIT_TEXT,
            'slug': NOTE_SLUG,
        }

        self.other_client.post(NOTE_EDIT_URL, data=form_data)

        self.note.refresh_from_db()
        self.assertEqual(self.note.title, original_title)
        self.assertEqual(self.note.text, original_text)

    def test_foreign_user_post_delete_does_not_remove_note_from_db(self):
        note_pk = self.note.pk
        expected_title = self.note.title
        expected_author = self.author

        self.other_client.post(NOTE_DELETE_URL)

        self.assertTrue(Note.objects.filter(pk=note_pk).exists())
        note = Note.objects.get(pk=note_pk)
        self.assertEqual(note.title, expected_title)
        self.assertEqual(note.author, expected_author)


class TestDuplicateSlug(BaseNoteTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Note.objects.create(
            title=DUPLICATE_FIRST_TITLE,
            text=DEFAULT_TEXT,
            slug=DUPLICATE_SLUG,
            author=cls.author,
        )

    def test_cannot_create_note_with_existing_slug(self):
        form_data = {
            'title': DUPLICATE_SECOND_TITLE,
            'text': DUPLICATE_SECOND_TEXT,
            'slug': DUPLICATE_SLUG,
        }

        response = self.author_client.post(ADD_URL, data=form_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(Note.objects.filter(slug=DUPLICATE_SLUG).count(), 1)
