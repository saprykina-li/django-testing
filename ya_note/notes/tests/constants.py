from django.urls import reverse

HOME_VIEW = 'notes:home'
LIST_VIEW = 'notes:list'
SUCCESS_VIEW = 'notes:success'
ADD_VIEW = 'notes:add'
DETAIL_VIEW = 'notes:detail'
EDIT_VIEW = 'notes:edit'
DELETE_VIEW = 'notes:delete'
LOGIN_VIEW = 'users:login'
SIGNUP_VIEW = 'users:signup'
LOGOUT_VIEW = 'users:logout'

NOTE_SLUG = 'author-note-slug'
FOREIGN_SLUG = 'foreign-slug'
NEW_NOTE_SLUG = 'new-note-slug'
ANON_ATTEMPT_SLUG = 'anon-attempt'
DUPLICATE_SLUG = 'duplicate-slug'

NOTE_SLUG_KWARGS = {'slug': NOTE_SLUG}

NEW_TITLE = 'Новая заметка'
NEW_TEXT = 'Описание'
ANON_TITLE = 'Попытка'
DEFAULT_TEXT = 'Текст'
EDITED_TITLE = 'Обновлённый заголовок'
EDITED_TEXT = 'Новый текст'
FOREIGN_EDIT_TITLE = 'Попытка подмены заголовка'
FOREIGN_EDIT_TEXT = 'Попытка подмены текста'
DUPLICATE_FIRST_TITLE = 'Первая'
DUPLICATE_SECOND_TITLE = 'Вторая'
DUPLICATE_SECOND_TEXT = 'Другой текст'
SLUGIFIED_TITLE = 'Транслит заголовка'
FOREIGN_NOTE_TITLE = 'Чужая заметка'

HOME_URL = reverse(HOME_VIEW)
ADD_URL = reverse(ADD_VIEW)
LIST_URL = reverse(LIST_VIEW)
SUCCESS_URL = reverse(SUCCESS_VIEW)
LOGIN_URL = reverse(LOGIN_VIEW)
SIGNUP_URL = reverse(SIGNUP_VIEW)
LOGOUT_URL = reverse(LOGOUT_VIEW)
NOTE_DETAIL_URL = reverse(DETAIL_VIEW, kwargs=NOTE_SLUG_KWARGS)
NOTE_EDIT_URL = reverse(EDIT_VIEW, kwargs=NOTE_SLUG_KWARGS)
NOTE_DELETE_URL = reverse(DELETE_VIEW, kwargs=NOTE_SLUG_KWARGS)
