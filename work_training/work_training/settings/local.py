# -*- coding: utf-8 -*-
from .base import *
from django.utils.translation import ugettext_lazy as _

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


