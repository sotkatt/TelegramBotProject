import configparser
from pathlib import Path

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

BASE_DIR = Path(__file__).resolve().parent.parent

MY_DOMAIN = "http://127.0.0.1:8000"

SECRET_KEY = CONFIG['Django']['SECRET_KEY']

TOKEN_KEY = CONFIG['Telegram']['TOKEN_KEY']

DEBUG = True

LANGUAGE_CODE = CONFIG['Django']['LANGUAGE_CODE']

TIME_ZONE = CONFIG['Django']['TIME_ZONE']

USE_I18N = True

USE_TZ = True

STATIC_URL = CONFIG['Django']['STATIC_URL']

MEDIA_URL = CONFIG['Django']['MEDIA_URL']

MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = CONFIG['Django']['DEFAULT_AUTO_FIELD']

ROOT_URLCONF = CONFIG['Django']['ROOT_URLCONF']

WSGI_APPLICATION = CONFIG['Django']['WSGI_APPLICATION']

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



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
            ],
        },
    },
]

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

