"""
Django settings for MotorMSRGeoTrackingProject project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')jr^w6$(tn_+hw06adoe3*1q%do*#4v617nz4no7vavh#)ru)q'

# Close the session when user closes the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '192.168.101.121', '192.168.100.61', '116.68.205.72', 'mis.digital', '192.168.101.188']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'MotorMSRGeoTrackingApp',
    'channels'
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "MotorMSRGeoTrackingProject.parent_routing.channel_routing",
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MotorMSRGeoTrackingProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'MotorMSRGeoTrackingProject.wsgi.application'
#ASGI_APPLICATION = "MotorMSRGeoTrackingProject.parent_routing.channel_routing"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'MotorDashboard': {
        'NAME': 'MotorDashboard',
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.100.61',
        'USER': 'sa',
        'PASSWORD': 'dataport',  #'PASSWORD': 'flexiload',
        'OPTIONS': {
            'driver' : 'SQL Server Native Client 11.0',
            'driver_supports_utf8' : 'True',
            'use_legacy_date_fields': 'True'
        }
    },
    'DCR': {
        'NAME': 'DCR',
        'ENGINE': 'sql_server.pyodbc',
        'HOST': '192.168.100.75',
        'USER': 'sa',
        'PASSWORD': 'dataport',  #'PASSWORD': 'flexiload',
        'OPTIONS': {
            'driver' : 'SQL Server Native Client 11.0',
            'driver_supports_utf8' : 'True',
            'use_legacy_date_fields': 'True'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
