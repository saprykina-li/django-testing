from django.urls import reverse

NEWS_HOME_URL_NAME = 'news:home'
NEWS_DETAIL_URL_NAME = 'news:detail'
NEWS_COMMENT_EDIT_URL_NAME = 'news:edit'
NEWS_COMMENT_DELETE_URL_NAME = 'news:delete'

USERS_LOGIN_URL_NAME = 'users:login'
USERS_SIGNUP_URL_NAME = 'users:signup'
USERS_LOGOUT_URL_NAME = 'users:logout'

HOME_URL = reverse(NEWS_HOME_URL_NAME)
LOGIN_URL = reverse(USERS_LOGIN_URL_NAME)
SIGNUP_URL = reverse(USERS_SIGNUP_URL_NAME)
LOGOUT_URL = reverse(USERS_LOGOUT_URL_NAME)
