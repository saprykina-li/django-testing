from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

from notes.models import Note

User = get_user_model()


class BaseNoteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username='author',
            password='testpass123',
            email='author@example.com',
        )
        cls.other = User.objects.create_user(
            username='other',
            password='testpass123',
            email='other@example.com',
        )
        cls.note = Note.objects.create(
            title='Заметка автора',
            text='Текст заметки',
            slug='author-note-slug',
            author=cls.author,
        )

    def setUp(self):
        super().setUp()
        self.anonymous_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.other_client = Client()
        self.other_client.force_login(self.other)
