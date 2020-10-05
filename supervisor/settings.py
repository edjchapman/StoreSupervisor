"""
Django settings for supervisor project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTSIDE_PROJECT_DIR = os.path.dirname(BASE_DIR)

APPENV = os.getenv('APP_SETTINGS_ENV', "LOCAL")

# SECURITY WARNING: keep the secret key used in production secret!
if APPENV == 'LOCAL':
    SECRET_KEY = '0fjv68#3k4lqmfp@n=eormxy^t8mmv@*&i4rn7!@#i#a*+g^1$'
else:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

if APPENV == 'LOCAL':
    DEBUG = True
else:
    DEBUG = os.getenv('DJANGO_DEBUG', False)

if APPENV == 'LOCAL':
    ALLOWED_HOSTS = [
        '127.0.0.1'
    ]
else:
    ALLOWED_HOSTS = [
        os.getenv('DJANGO_ALLOWED_HOSTS')
    ]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'channels',
    'django_celery_beat',
    'report_builder',
    'report_builder_scheduled'
]

CUSTOM_APPS = [
    'platforms',
    'stores'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'supervisor.urls'

ADMINS = [("Ed", "edchapman88@gmail.com")]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'supervisor.wsgi.application'

ASGI_APPLICATION = "supervisor.routing.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if APPENV == 'LOCAL':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DJANGO_DEFAULT_DB_ENGINE'),
            'NAME': os.environ.get('DJANGO_DEFAULT_DB_NAME'),
            'HOST': os.environ.get('DJANGO_DEFAULT_DB_HOST'),
            'PORT': os.environ.get('DJANGO_DEFAULT_DB_PORT'),
            'USER': os.environ.get('DJANGO_DEFAULT_DB_USER'),
            'PASSWORD': os.environ.get('DJANGO_DEFAULT_DB_PASSWORD'),
            'OPTIONS': {
                'options': '-c search_path=supervisor,supervisor'
            }
        },
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# INTERNATIONALISATION
#
LANGUAGE_CODE = 'en-GB'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC/MEDIA
#
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(OUTSIDE_PROJECT_DIR, 'static')
STATICFILES_DIRS = ["templates/static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(OUTSIDE_PROJECT_DIR, 'media')

# CELERY
#
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# SMTP
#
EMAIL_HOST = "smtp.eu.mailgun.org"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

# LOGGING
#
LOG_DIR = OUTSIDE_PROJECT_DIR + '/logs/'

os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + 'info_logfile.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
        }
    }
}
