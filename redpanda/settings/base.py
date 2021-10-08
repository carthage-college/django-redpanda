# -*- coding: utf-8 -*-

"""Django settings for project."""

import datetime
import os

from djimix.settings.local import DBSERVERNAME
from djimix.settings.local import INFORMIX_ODBC
from djimix.settings.local import INFORMIX_ODBC_TRAIN
from djimix.settings.local import INFORMIXDIR
from djimix.settings.local import INFORMIXSERVER
from djimix.settings.local import INFORMIXSQLHOSTS
from djimix.settings.local import LD_LIBRARY_PATH
from djimix.settings.local import LD_RUN_PATH
from djimix.settings.local import MSSQL_EARL
from djimix.settings.local import ODBCINI
from djimix.settings.local import ONCONFIG

TERM = 'RA'
if datetime.date.today().month < 7:
    TERM = 'RC'

# Debug
DEBUG = False
INFORMIX_DEBUG = ''
REQUIRED_ATTRIBUTE = True
ADMINS = ()
MANAGERS = ADMINS
SECRET_KEY = None
ENCRYPTION_KEY = None
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
TIME_INPUT_FORMATS = ('%H:%M %p',)
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
API_URL = '{0}/{1}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{0}'.format(SERVER_URL)
ROOT_URLCONF = 'redpanda.core.urls'
WSGI_APPLICATION = 'redpanda.wsgi.application'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = BASE_DIR
PROJECT_APP = os.path.basename(BASE_DIR)
ROOT_URL = '/{0}/'.format(PROJECT_APP)
ADMIN_MEDIA_PREFIX = '/static/admin/'
MEDIA_ROOT = '{0}/assets/'.format(ROOT_DIR)
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = '/static/{0}/'.format(PROJECT_APP)
MEDIA_URL = '/media/{0}/'.format(PROJECT_APP)
FILE_UPLOAD_PERMISSIONS = 0o644
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_redpanda',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
    },
}
INSTALLED_APPS = (
    'bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # apps
    'redpanda.lynx',
    'redpanda.core',
    'redpanda.research',
    # needed for template tags
    'djtools',
    # honeypot for admin attacks
    'admin_honeypot',
    # needed for template tags and error views
    #'djtools',
    # sign in as a user
    'loginas',
    # tagging package
    'taggit',
)
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'redpanda.core.middleware.UserTypeMiddleware',
)
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            '/data2/django_templates/',
            '/data2/django_templates/djcher/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 604800,
        'KEY_PREFIX': '{0}_'.format(PROJECT_APP),
    }
}
ADMIN_GROUP = ''
ATHLETICS_GROUP = ''
FACULTY_GROUP = ''
RESEARCH_GROUP = ''
STAFF_GROUP = ''
STUDENT_GROUP = ''
ALL_GROUPS = (
    (FACULTY_GROUP, 'Faculty'),
    (STAFF_GROUP, 'Staff'),
    (STUDENT_GROUP, 'Students'),
    (ATHLETICS_GROUP, 'Athletics'),
    (ADMIN_GROUP, 'Admin'),
    (RESEARCH_GROUP, 'Research'),
)
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = None
LDAP_OBJECT_CLASS = ''
LDAP_GROUPS = None
LDAP_RETURN = ()
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{0}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_DOMAIN = ''
SESSION_COOKIE_NAME = 'django_redpanda_cookie'
SESSION_COOKIE_AGE = 31536000  # 1 year
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# logging
LOG_FILEPATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/',
)
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
DEBUG_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
INFO_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'info.log')
ERROR_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'error.log')
CUSTOM_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'custom.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'custom_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': CUSTOM_LOG_FILENAME,
            'formatter': 'custom',
        },
        'info_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'maxBytes': 50000,
            'filename': INFO_LOG_FILENAME,
            'formatter': 'simple',
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
# app constants
START_DATE = datetime.datetime(datetime.datetime.now().year, 6, 1)
START_DATE_VAX = datetime.datetime(2021, 7, 1)
SPORTS_MONTH = 5
# reminder messages
REDPANDA_TEST_CIDS = ()
REDPANDA_SERVER_URL = ''
REDPANDA_ROOT_URL = '/'
REDPANDA_SHORT_URL_API = 'lynx/api/'
REDPANDA_FACSTAFF_TO_LIST = []
REDPANDA_SURVEY_FORM = ''
##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local import *", we use exec so that
# local has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

phile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local.py')
if os.path.exists(phile):
    import imp
    import sys
    module_name = '{0}.settings.local'.format(PROJECT_APP)
    module = imp.new_module(module_name)
    module.__file__ = phile
    sys.modules[module_name] = module
    exec(open(phile, 'rb').read())
