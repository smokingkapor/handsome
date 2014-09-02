# -*- coding: utf-8 -*-
"""
Django settings for handsome project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1

ADMINS = (('Kapor Zhu', 'smokingkapor@gmail.com'),)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tdi&3^4%_yy9)eveyqx_=(@t#ko0g**9m)$h+gfivgth3(r4%l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

LOCAL_APPS = (
    'accounts',
    'clothings',
    'designs',
    'deliveries',
    'handsome',
    'orders',
    'payments',
    'portals',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd libs
    'compressor',
    'easy_thumbnails',
    'south',
) + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'handsome.urls'

WSGI_APPLICATION = 'handsome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'handsome',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

THUMBNAIL_ALIASES = {
    '': {
        'small': {
            'size': (128, 128)
        },
        'medium': {
            'size': (256, 256)
        },
        'large': {
            'size': (512, 512)
        },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ygrass.system.notification@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = u'[优草]'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'ygrass.system.notification@gmail.com'

LOGIN_URL = '/accounts/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

SMS_NOTIFICATION_ENABLED = False
SMS_SERVER_URL = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit'
SMS_SERVER_USERNAME = ''
SMS_SERVER_PASSWORD = ''
SMS_TEMPLATES = {
    'designed': u'设计师{}已经为您量身搭配了多套服装，请登录优草(ygrass.com)查看.',
    'temporary_pwd': u'您在优草的动态密码是{}，三十分钟内有效.'
}

ALIPAY_PID = ''
ALIPAY_KEY = ''
ALIPAY_EMAIL = ''

try:
    from local_settings import *  # noqa
except ImportError:
    pass
