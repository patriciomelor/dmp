"""
Django settings for dmp project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
import dj_database_url
from pathlib import Path
from django.urls import reverse_lazy
from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "1"

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "1"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,plannit-app.cl,165.232.156.255").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'import_export',
    'crispy_forms',    
    'debug_toolbar',
    # 'easy_thumbnails',
    # 'filer',
    # 'mptt',
    # 'multiupload',
    'django_filters',
    'formtools',
    'rest_framework',
    'rest_framework.authtoken',
    'invitations',
    'django_summernote',
    'django_celery_beat',
    'storages',
    
    'dashboard',
    'tools',
    'notifications',
    'panel_carga',
    'bandeja_es',
    'configuracion',
    'buscador',
    'status',
    'status_encargado',
    'analitica',
    

]


# Digital Ocean's AWS s3 Storage (Spaces)

# AWS_S3_ENDPOINT_URL = "sfo3.digitaloceanspaces.com"

# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# AWS_LOCATION = "https://plannit-spaces.sfo3.digitaloceanspaces.com/"

# DEFAULT_FILE_STORAGE = "dmp.cdn.backends.StaticRootS3Boto3Storage"
# STATICFILE_STORAGE = "dmp.cdn.backends.MediaRootS3Boto3Storage"

# AUTH_USER_MODEL = 'dashboard.Usuario'

SITE_ID = 3

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Allauth methods
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True


LOGIN_URL = reverse_lazy("account_login")

CELERY_TIMEZONE = 'America/Santiago'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

APPEND_SLASH = False

# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'dmp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',                
            ],
        },
    },
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

# EMAIL SETTINGS

EMAIL_HOST = 'mail.stod.cl'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dmp@stod.cl'
EMAIL_HOST_PASSWORD = 'dmp.2020'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'dmp@stod.cl'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


WSGI_APPLICATION = 'dmp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if DEVELOPMENT_MODE is True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dmpdb5',
            'USER': 'postgres',
            'PASSWORD': 'dmp.2020',
            'HOST': os.getenv("DATABASE_URL", "134.209.78.27"),
            'PORT': 5432,
            'SSLMODE': 'require',
            'DISABLE_SERVER_SIDE_CURSORS': True,
        }
    }

else:
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'PLANNIT',
            'USER': 'postgres',
            'PASSWORD': 'dmp.2020',
            'HOST': os.getenv("DATABASE_URL", "134.209.78.27"),
            'PORT': 5432,
            'SSLMODE': 'require',
            'DISABLE_SERVER_SIDE_CURSORS': True,
        }
    }



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators


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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'
_ = lambda s: s

LANGUAGES = (
 ('es', _('Espanish')),
 ('zh', _('Chinese')),
 ('en', _('English')),
)

TIME_ZONE = 'America/Santiago'


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/



# Add Digital Ocean's Spaces Config Variables
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATICFILES_DIRS = (BASE_DIR / 'static',)

USE_SPACES = os.getenv("USE_SPACES", "0")  == "1"
if USE_SPACES:
    from .cdn.conf import *
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATIC_URL = '/static/'
    MEDIA_ROOT = BASE_DIR / 'static/media'
    MEDIA_URL = '/media/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'static/media'



MESSAGE_TAGS = {
    messages.DEBUG: 'alert alert-bordered alert-info',
    messages.INFO: 'alert alert-bordered alert-info',
    messages.SUCCESS: 'alert alert-bordered alert-success',
    messages.WARNING: 'alert alert-bordered alert-warning',
    messages.ERROR: 'alert alert-bordered alert-warning',
}
#summernote
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    'iframe': False,

    # You can put custom Summernote settings
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)
        'lang': 'es-ES',

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],


        # You can also add custom settings for external plugins
        'print': {
            'stylesheetUrl': '/some_static_folder/printable.css',
        },
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            'theme': 'monokai',
        },
    },

    # Require users to be authenticated for uploading attachments.
    'attachment_require_authentication': True,

    # You can completely disable the attachment feature.
    'disable_attachment': False,

    # Set to `True` to return attachment paths in absolute URIs.
    'attachment_absolute_uri': False,

}