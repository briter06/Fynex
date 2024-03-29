"""
Django settings for Fynex project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import sys
import environ

env = environ.Env()
environ.Env.read_env()


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'fynexhealth@gmail.com'
EMAIL_DISPLAY_NAME = 'Fynex'
DEFAULT_FROM_EMAIL = EMAIL_DISPLAY_NAME+' <'+EMAIL_HOST_USER+'>'
EMAIL_HOST_PASSWORD = env('FYNEX_EMAIL_PASSWORD')




COS_ENDPOINT = env('COS_ENDPOINT')
COS_API_KEY_ID = env('COS_API_KEY_ID')
COS_INSTANCE_CRN = env('COS_INSTANCE_CRN')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('secret_key_fynex')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['fynexapp.herokuapp.com','localhost','*']


# Application definition

INSTALLED_APPS = [
    'captcha',
    'channels',
    'datetimeutc',
    'fynex_app.apps.FynexAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
ROOT_URLCONF = 'Fynex.urls'

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

WSGI_APPLICATION = 'Fynex.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'de5b8tedtgov62',

        'USER': 'fgzqowewizrzco',

        'PASSWORD': '0dc390f611d3b40f4fa864f05c6872d457a9f2e4446e4587f1e8b9752dfe1507',

        'HOST': 'ec2-52-7-115-250.compute-1.amazonaws.com',

        'PORT': '5432',

        'TEST':{
            'NAME': 'de5b8tedtgov62',

            'USER': 'fgzqowewizrzco',

            'PASSWORD': '0dc390f611d3b40f4fa864f05c6872d457a9f2e4446e4587f1e8b9752dfe1507',

            'HOST': 'ec2-52-7-115-250.compute-1.amazonaws.com',

            'PORT': '5432'
        }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CAPTCHA = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "fynex_app/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

RECOMMENDER_ROOT = os.path.join(BASE_DIR, 'fynex_app/recommender')


ASGI_APPLICATION = "Fynex.routing.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')],
        },
    },
}

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

TIME_ZONE = 'America/Bogota'
USE_TZ = True