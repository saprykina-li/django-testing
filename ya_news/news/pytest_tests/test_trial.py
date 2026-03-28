import pytest

from news.models import News

pytestmark = pytest.mark.skip(
    reason='Экспериментальный код, не нужен для тестов',
)

TITLE = 'Заголовок новости'
TEXT = 'Тестовый текст'


@pytest.fixture
def trial_news(db):
    return News.objects.create(title=TITLE, text=TEXT)


@pytest.mark.django_db
def test_successful_creation(trial_news):
    assert News.objects.count() == 1


@pytest.mark.django_db
def test_title(trial_news):
    assert trial_news.title == TITLE
