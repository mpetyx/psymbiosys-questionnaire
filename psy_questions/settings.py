# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

if os.environ.get('LOGNAME') in ['3nvi', 'psy-dev']:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'questionnaire',                      # Or path to database file if using sqlite3.
            'USER': 'postgres',                      # Not used with sqlite3.
            'PASSWORD': '1234',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    import dj_database_url

    DATABASES = dict()
    DATABASES['default'] = dj_database_url.config()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# psy_questions: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# psy_questionss: "http://media.lawrence.com", "http://psy_questions.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# psy_questionss: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j69g6-&t0l43f06iq=+u!ni)9n)g!ygy4dk-dgdbrbdx7%9l*6'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# psy_questions: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# URL prefix for static files.
# psy_questions: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
# STATICFILES_DIRS = (
#     os.path.abspath('./static'),
#     os.path.abspath('static'),
#     os.path.join(BASE_DIR, 'static'),
#     # os.path.abspath('../questionnaire/static/')
# )

# List of finder classes that know how to find static files in
# various locations.
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'questionnaire.request_cache.RequestCacheMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'psy_questions.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'questionnaire/templates'),
    os.path.join(BASE_DIR, 'psy_questions/templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'questionnaire',
    'django.contrib.admin',
    'transmeta',
    'questionnaire.page',
    'email_campaigns',
    'multi_email_field',
    'widget_tweaks'
)

LANGUAGES = (
    ('en', 'English'),
    # ('de', 'Deutsch'),
)

# Defines the progressbar behavior in the questionnaire
# the possible options are 'default', 'async' and 'none'
#
#   'default'
#   The progressbar will be rendered in each questionset together with the
#   questions. This is a good choice for smaller questionnaires as the
#   progressbar will always be up to date.
#
#   'async'
#   The progressbar value is updated using ajax once the questions have been
#   rendered. This approach is the right choice for bigger questionnaires which
#   result in a long time spent on updating the progressbar with each request.
#   (The progress calculation is by far the most time consuming method in
#    bigger questionnaires as all questionsets and questions need to be
#    parsed to decide if they play a role in the current run or not)
#
#   'none'
#   Completely omits the progressbar. Good if you don't want one or if the
#   questionnaire is so huge that even the ajax request takes too long.
QUESTIONNAIRE_PROGRESS = ''

# Defines how the questionnaire and questionset id are passed around.
# If False, the default value, the ids are part of the URLs and visible to the
# user answering the questions.
# If True the ids are set in the session and the URL remains unchanged as the
# user goes through the steps of the question set.
QUESTIONNAIRE_USE_SESSION = False

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = os.environ.get("MAILGUN_ACCESS_KEY","key-726951")
MAILGUN_SERVER_NAME = 'psymbiosys.info'

LOGIN_URL = '/analytics/login/'