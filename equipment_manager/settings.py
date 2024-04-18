"""
Django settings for equipment_manager project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

VIRTUAL_HOSTS = config("VIRTUAL_HOST", "localhost").split(",")

# Allow connections from both localhost & any domain name hosts nginx is serving this app under
ALLOWED_HOSTS = ["localhost", "127.0.0.1"] + VIRTUAL_HOSTS

# Let's django know the domain's that the reverse proxy is serving are allowed
CSRF_TRUSTED_ORIGINS = [f"https://{url}" for url in ALLOWED_HOSTS]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_bootstrap5",
    "widget_tweaks",
    'haystack',
    'equipment_app',
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

ROOT_URLCONF = 'equipment_manager.urls'

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

WSGI_APPLICATION = 'equipment_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
# If needed, this can be re-enabled
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    "default" : {
        "ENGINE": "django.db.backends.postgresql",
        "NAME" : config("POSTGRES_DB"),
        "USER" : config("POSTGRES_USER"),
        "PASSWORD" : config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", default=5432),
        # In the name of security, do not allow non TLS connections to the database
        'OPTIONS': {'sslmode': 'verify-full', "sslrootcert" : "system"},
    }
}

#HayStack 
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine',
        'URL': config("ELS_HOST"),
        'INDEX_NAME': 'haystack',
        'KWARGS' : {
            'http_auth' : ("elastic", config("ELS_PASS")),
            'use_ssl' : True,
            'ca_certs' : config("ELS_ROOT_CA")
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT= 'static_collect'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

#Storages
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        "OPTIONS": {
        },
    },
}

# Checking and settting up the default storage for media
if(config("S3_BUCKET_NAME", default="") != ""):
    STORAGES["default"] ={
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
        },
    }
    # Reads from a .env file to credientals and the hostname of the S3 server
    AWS_STORAGE_BUCKET_NAME = config("S3_BUCKET_NAME")
    AWS_S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY")
    AWS_S3_SECRET_ACCESS_KEY = config("S3_SECRET_KEY")
    AWS_S3_CUSTOM_DOMAIN = config("S3_HOST")
    AWS_S3_ENDPOINT_URL = config("S3_HOST")

    #NEVER try to connect to an AWS server without TLS
    AWS_S3_USE_SSL = True
    # If a root ca is specified, AWS_S3_VERIFY will use that certificate
    # Otherswise, setting ASW_S3_VERIFY to true will have the backend library check against amazon's CA
    AWS_S3_VERIFY = True if (CA := config("S3_ROOT_CA", default="")) == "" else CA
    #The media url is no longer a resource django serves
    MEDIA_URL = config("S3_HOST") + "/" + config("S3_BUCKET_NAME") + "/"
elif (PotentialMediaLocation := config("MEDIA_LOCATION", default="")) == "":
    # If there is no MEDIA_LOCATION specified
    MEDIA_ROOT = BASE_DIR / 'media'
    MEDIA_URL = 'media/'
else:
    # If there is a MEDIA_LOCATION, use that one
    MEDIA_ROOT = os.path.join(PotentialMediaLocation, VIRTUAL_HOSTS[0])
    MEDIA_URL = 'media/'

# For when Django is behind nginx to serve dynamic content


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Bootstrap Settings
BOOTSTRAP5 = {
    #I specified these versions as they are newer than what the packacke auto-includes
    "css_url" : {
        "url" : "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "integrity" : "sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
        "crossorigin" : "anonymous",
    },
    "javascript_url" : {
        "url" : "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js",
        "integrity" : "sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+",
        "crossorigin" : "anonymous"
    }
}