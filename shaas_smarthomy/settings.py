"""
Django settings for shaas_smarthomy project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5l@7xev*kj-9=g*0_&5m30%$lbb9-%ib)zg!n*6wf!0adc%c=2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'services.smarthomy.com']


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'security.apps.SecurityConfig',
    'oauth2_provider',
    'rest_framework',
    'drf_yasg',
    'django_celery_results',
    'dpa_chile',
    'corsheaders',
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

ROOT_URLCONF = 'shaas_smarthomy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'shaas_smarthomy.wsgi.application'

ASGI_APPLICATION = 'shaas_smarthomy.asgi.application'

# Configuración de Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://default:n5HN6DqQ0rxXEbBZhP51Y2ZuWb9QpnP0@redis-14397.c60.us-west-1-2.ec2.cloud.redislabs.com:14397")],
        },
    },
}


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smarthomydb',
        'USER': 'root',
        'PASSWORD': '2a5les2a',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                },
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'smarthomy$smarthomydb',
    #     'USER': 'smarthomy',
    #     'PASSWORD': '2a5les2a',
    #     'HOST': 'smarthomy.mysql.pythonanywhere-services.com',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    #             },
    # }
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

CORS_ALLOW_ALL_ORIGINS = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = True


#   Static files (CSS, JavaScript, Images)
#   https://docs.djangoproject.com/en/3.1/howto/static-files/

#   STATIC_ROOT = "/home/smarthomy/shaas_smarthomy/static"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = '/static/'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'ACCESS_TOKEN_EXPIRE_SECONDS': 7200,
}

#   CELERY related settings
#   CELERY_BROKER_URL = 'redis://smarthomy:$martHomy2022@redis-16290.c60.us-west-1-2.ec2.cloud.redislabs.com:16290/0'
CELERY_BROKER_URL = 'redis://localhost:6379'

#   CELERY_RESULT_BACKEND = 'redis://smarthomy:$martHomy2022@redis-16290.c60.us-west-1-2.ec2.cloud.redislabs.com:16290/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Santiago'
BROKER_POOL_LIMIT = 0
CELERY_TASK_TRACK_STARTED = True
CANCEL_TASKS_BY_DEFAULT = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'


GRAPPELLI_AUTOCOMPLETE_LIMIT = 10
GRAPPELLI_ADMIN_TITLE = "Smart Homy Services"

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "main": {
        "Subscription": ("username__iexact", "name__icontains",)
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = 'mensajeria@smarthomy.com'   #'juan@smarthomy.com'
EMAIL_HOST_PASSWORD = '$martHomy2022'       #'Summoning87'
EMAIL_PORT = 587
SERVER_EMAIL = EMAIL_HOST_USER
