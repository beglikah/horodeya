"""
Django settings for horodeya project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

if len(sys.argv) > 0 and sys.argv[1] == 'test':
    TEST = True
else:
    TEST = False

if TEST:
    SECRET_KEY = 'testing'
else:
    SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', '.horodeya.org']

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',

    'rules',
    'tempus_dominus',
    'bootstrap4',
    'projects.apps.ProjectsConfig',
    'home.apps.HomeConfig',
    
    'anymail',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'django.contrib.sites', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Wagtail http://docs.wagtail.io/en/v2.6.2/getting_started/integrating_into_django.html
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'debug_toolbar',
    'vote',
    
    'photologue',
    'sortedm2m',

    'django.contrib.humanize',
]

if not TEST:
    INSTALLED_APPS += ['stream_django']


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'horodeya.force_default_language_middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Wagtail http://docs.wagtail.io/en/v2.6.2/getting_started/integrating_into_django.html
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'horodeya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'horodeya.context_processors.stream_token',
            ],
        },
    },
]

WSGI_APPLICATION = 'horodeya.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Wagtail
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

WAGTAIL_SITE_NAME = 'Хородея'
WAGTAIL_FRONTEND_LOGIN_URL = '/accounts/login/'

BOOTSTRAP4 = {
    'theme_url': None
}

SITE_ID = 1

# allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USER_DISPLAY = lambda u: u.first_name
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_FORMS = {'signup': 'home.forms.NamesSignupForm'}

BOOTSTRAP4 = {
    "css_url": '/static/css/bootstrap.min.css',
    'javascript_url': '/static/js/bootstrap.min.js',
    'jquery_url': '/static/js/jquery-3.4.1.min.js',
    'jquery_slim_url': '/static/js/jquery-3.4.1.min.js',
    'popper_url': '/static/js/popper.min.js',
}

EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
DEFAULT_FROM_EMAIL = "info@horodeya.org"
SERVER_EMAIL = "ops@horodeya.org"

ANYMAIL = {
    'WEBHOOK_SECRET': os.getenv('ANYMAIL_WEBHOOK_SECRET')
}


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')

AUTH_USER_MODEL = 'projects.User'

LANGUAGE_CODE = 'bg-bg'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'locale-allauth')
]

TEMPUS_DOMINUS_INCLUDE_ASSETS = True

INTERNAL_IPS = [
    '127.0.0.1',
]

STREAM_API_KEY = os.getenv('STREAM_API_KEY')
STREAM_API_SECRET = os.getenv('STREAM_API_SECRET')

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:m:s'

LANGUAGES = (
    ('en', 'English'),
    ('bg', 'Бъларски')
)
