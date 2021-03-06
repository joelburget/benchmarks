import os
import django
import platform
import socket

# Django settings for benchmarks project.
AUTH_PROFILE_MODULE = 'users.UserProfile'

# Set up relative paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__)) # path to the django installation
SITE_ROOT = os.path.dirname(os.path.realpath(__file__)) # path to the project directory

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Joel Burget', 'burget.6@osu.edu'),
    ('Colin Drake', 'drake.248@osu.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
      #sqlite3 for now
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'db') + '/development.db',                      # Or path to gatabase file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Detroit'#'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dx6v@!nsn==jy$&$7i#fljdxty47yu%9rl!6zexhm^&wgwacbu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'benchmarks.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'django.contrib.comments',
    'django.contrib.admin',
    'django.contrib.markup',
    'benchmarks.groups',
    'benchmarks.posts',
    'benchmarks.users',
    'benchmarks.extended_comments',
    'benchmarks.flup',
    'benchmarks.templatetags',
		'benchmarks.reversion',
)

COMMENTS_APP = 'benchmarks.extended_comments'
COMPRESS = True

# django.core.mail Setup
# Used for registration purposes
EMAIL_ENABLED = False

try:
  import email_settings
except ImportError:
  # This is okay, eg. if we are in the development environment
  pass
else:
  EMAIL_USE_TLS = email_settings.EMAIL_USE_TLS
  EMAIL_HOST = email_settings.EMAIL_HOST
  EMAIL_HOST_USER = email_settings.EMAIL_HOST_USER
  EMAIL_HOST_PASSWORD = email_settings.EMAIL_HOST_PASSWORD
  EMAIL_PORT = email_settings.EMAIL_PORT
  ADMIN_EMAIL = email_settings.ADMIN_EMAIL
  SERVER_EMAIL = ADMIN_EMAIL
  EMAIL_ENABLED = True

# Server-specific lines
host = platform.node()

if host == 'syrus.cse.ohio-state.edu':
  FORCE_SCRIPT_NAME = ''
  DEBUG = False
  SITE_URL = 'resolve.cse.ohio-state.edu'
else:
  SITE_URL = '127.0.0.1:8888'
