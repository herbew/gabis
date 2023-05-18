"""
Base settings to build other settings files upon.
"""

import environ, os

from datetime import datetime

from django.utils.translation import gettext_lazy as _
from qr_code.qrcode import constants


# Path service apps (gabis/config/settings/base.py - 3 = gabis/)
ROOT_DIR = environ.Path(__file__) - 3  
APPS_DIR = ROOT_DIR.path('gabis')

# Environment File Settingst
ENV_FILE = os.path.join(os.path.dirname(__file__), '../../.env')

env = environ.Env()
environ.Env.read_env(ENV_FILE)

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)
# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# DATABASES = {
#     'default': env.db(default='postgis://postgres:postgres@postgres:5432/postgres')
# }

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///db_gabis'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'

# WSGI
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # Handy template tags
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'modeltranslation',
    'crispy_forms',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
#     'allauth.socialaccount.providers.google',
#     'allauth.socialaccount.providers.facebook'
    'gabis.libs.templated_docs.apps.TemplatedDocsConfig',
    'gabis.libs.avatar.apps.AvatarConfig',
    'gabis.libs.django_messages.apps.DjangoMessagesConfig',
    'import_export',
    'qr_code',
     
]

LOCAL_APPS = [
    'gabis.core',
    'gabis.apps.users.apps.UsersAppConfig',
    'gabis.apps.masters.apps.MastersAppConfig',
    'gabis.apps.schedules.apps.SchedulesAppConfig',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
# TIME_ZONE = 'UTC'
#TIME_ZONE = "Asia/Jakarta"


LOCALE_PATHS = (
    os.path.join(str(APPS_DIR), 'locale'),

)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
     'sites': 'gabis.libs.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    # Django
    'django.contrib.auth.backends.ModelBackend',
    
    # Django Allauth Backend
    'allauth.account.auth_backends.AuthenticationBackend',
    
    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
   
    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'users:redirect'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'



# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'gabis.apps.masters.middleware.GabisLocaleMiddleware'
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],

        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # https://pypi.org/project/django-rest-framework-social-oauth2/
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'SAMEORIGIN' #'DENY'



# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Heribertus Rustyawan""", 'herbew@gmail.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# NOTIFICATIONS OVERRIDE
# https://pypi.org/project/django-notifications-hq/1.0/
# -------------------------------------------------------------------------------
NOTIFICATIONS_SOFT_DELETE = True

HOST_EMAIL_NOTIFICATION = 'http://thepucukan.com/'

LANGUAGES = (
    ('ar', _('Arabic')),
    ('en-us', _('English')),
    ('ja', _('Japanese')),
    ('ko', _('Korean')),
    ('hi', _('Hindi')),
    ('es', _('Spanish')),
    
)

MULTILINGUAL_LANGUAGES = (
    "ja",
    "en-us",
    'ar',
    'ko',
    'hi',
    'es'
)
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
TIME_ZONE = env('TIME_ZONE', default='UTC')

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'gabis.apps.users.adapters.AccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'gabis.apps.users.adapters.SocialAccountAdapter'

INSTALLED_APPS += ['sass_processor']
STATICFILES_FINDERS += ['sass_processor.finders.CssFinder']
SASS_PROCESSOR_AUTO_INCLUDE = False
SASS_PRECISION = 8

# ACCOUNTS override
# ------------------------------------------------------------------------------
ACCOUNT_FORMS = {
    'signup':'gabis.apps.accounts.forms.SignupForm',
    'login':'gabis.apps.accounts.forms.LoginForm',
    'change_password': 'gabis.apps.accounts.forms.ChangePasswordForm',
    'set_password': 'gabis.apps.accounts.forms.SetPasswordForm',
    'reset_password_from_key': 'gabis.apps.accounts.forms.ResetPasswordKeyForm',
}


# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL', default='redis://127.0.0.1:6379'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    },
    
    # QR-Code
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    }
    
}

QR_CODE_CACHE_ALIAS = 'qr-code'

QR_CODE_URL_PROTECTION = {
    constants.TOKEN_LENGTH: 30,                         # Optional random token length for URL protection. Defaults to 20.
    constants.SIGNING_KEY: 'my-secret-signing-key',     # Optional signing key for URL token. Uses SECRET_KEY if not defined.
    constants.SIGNING_SALT: 'my-signing-salt',          # Optional signing salt for URL token.
    constants.ALLOWS_EXTERNAL_REQUESTS_FOR_REGISTERED_USER: True,  # Tells whether a registered user can request the QR code URLs from outside a site that uses this app. It can be a boolean value used for any user or a callable that takes a user as parameter. Defaults to False (nobody can access the URL without the signature token).
    
}




# EMAIL
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['anymail']

# EMAIL
# ------------------------------------------------------------------------------

DEFAULT_FROM_EMAIL = env(
     'DJANGO_DEFAULT_FROM_EMAIL',
     default='Simple Account<noreply@thepucukan.com>'
 )

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[SimpleAccount]')
 


# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

ANYMAIL = {
    "MAILJET_API_KEY":env('MAILJET_API_KEY', default=""),
    "MAILJET_SECRET_KEY": env('MAILJET_SECRET_KEY', default=""),
    }
    
MAILJET_API_URL = "https://api.mailjet.com/v3.1/"


# SOCIAL MEDIA ACCOUNT ACCESS
# ==============================================================================
# Google configuration
# https://pypi.org/project/django-rest-framework-social-oauth2/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

INSTALLED_APPS += [
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2'
    ]

# AVATAR SETUP
# -------------------------------------------------------------------------------
DEFAULT_MALE_URL = 'gabis/images/default-avatar-men.png'
DEFAULT_FEMALE_URL = 'gabis/images/default-avatar-women.png'

# https://django-modeltranslation.readthedocs.io/_/downloads/en/latest/pdf/
MODELTRANSLATION_DEFAULT_LANGUAGE = "en_us" #"en_us"
MODELTRANSLATION_LANGUAGES = ('en_us','ja', 'ar', 'ko', 'hi',  'es')

MODELTRANSLATION_FALLBACK_LANGUAGES = dict(
    default=MODELTRANSLATION_LANGUAGES,
    )
 
MODELTRANSLATION_PREPOPULATE_LANGUAGE = "en_us"

MODELTRANSLATION_TRANSLATION_FILES = (
    'gabis.apps.users.translation',
    'gabis.apps.masters.translation',
    'gabis.apps.schedules.translation',
    )

# MODELTRANSLATION_CUSTOM_FIELDS = (
#     'code',
#     'name', 
#     'description'
#     )

MODELTRANSLATION_AUTO_POPULATE = True
MODELTRANSLATION_DEBUG = True




